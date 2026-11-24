from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any

import bambulabs_api as bl

CONFIG_DIR = Path.home() / ".bambu-cli"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_BAMBU_STUDIO_PATHS = [
    Path(r"C:\Program Files\Bambu Studio\bambu-studio.exe"),
    Path(r"C:\Program Files (x86)\Bambu Studio\bambu-studio.exe"),
]


def load_config() -> dict[str, Any]:
    if CONFIG_FILE.exists():
        try:
            return json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def save_config(cfg: dict[str, Any]) -> None:
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.write_text(json.dumps(cfg, indent=2, ensure_ascii=False), encoding="utf-8")


def find_bambu_studio(cfg: dict[str, Any], override: str | None = None) -> Path:
    if override:
        p = Path(override)
        if p.exists():
            return p
        raise FileNotFoundError(f"Bambu Studio が見つかりません: {p}")

    if cfg.get("bambu_studio_path"):
        p = Path(cfg["bambu_studio_path"])
        if p.exists():
            return p

    which = shutil.which("bambu-studio") or shutil.which("bambu-studio.exe")
    if which:
        return Path(which)

    for candidate in DEFAULT_BAMBU_STUDIO_PATHS:
        if candidate.exists():
            return candidate

    raise FileNotFoundError(
        "bambu-studio.exe が見つかりません。Bambu Studio をインストールするか、"
        "`bambu-cli config --bambu-studio <パス>` で指定してください。"
    )


def resolve_credentials(args: argparse.Namespace, cfg: dict[str, Any]) -> tuple[str, str, str]:
    ip = args.ip or os.environ.get("BAMBU_IP") or cfg.get("ip")
    access_code = args.access_code or os.environ.get("BAMBU_ACCESS_CODE") or cfg.get("access_code")
    serial = args.serial or os.environ.get("BAMBU_SERIAL") or cfg.get("serial")

    missing = []
    if not ip:
        missing.append("--ip (または BAMBU_IP)")
    if not access_code:
        missing.append("--access-code (または BAMBU_ACCESS_CODE)")
    if not serial:
        missing.append("--serial (または BAMBU_SERIAL)")

    if missing:
        print(
            "エラー: プリンター接続情報が不足しています: " + ", ".join(missing),
            file=sys.stderr,
        )
        print(
            "先に `bambu-cli config --ip <IP> --access-code <CODE> --serial <SERIAL>` を実行してください。",
            file=sys.stderr,
        )
        sys.exit(1)

    return ip, access_code, serial


def connect_mqtt(ip: str, access_code: str, serial: str, timeout: float = 10.0) -> bl.Printer:
    printer = bl.Printer(ip, access_code, serial)
    printer.mqtt_start()

    deadline = time.time() + timeout
    while time.time() < deadline:
        if printer.mqtt_client_ready():
            return printer
        time.sleep(0.25)

    # Fallback: connected but not yet received first status dump
    if printer.mqtt_client_connected():
        time.sleep(1.0)
        return printer

    printer.mqtt_stop()
    raise TimeoutError(
        f"プリンター ({ip}) への MQTT 接続がタイムアウトしました。"
        "LAN Only モード / Developer Mode が有効か、IP・Access Code・Serial が正しいか確認してください。"
    )


def run_slice(
    input_file: Path,
    bambu_studio: Path,
    output_dir: Path,
    settings: str | None = None,
    filaments: str | None = None,
    plate: int = 0,
    extra_args: list[str] | None = None,
) -> Path:
    if not input_file.exists():
        raise FileNotFoundError(f"入力ファイルが見つかりません: {input_file}")

    output_dir.mkdir(parents=True, exist_ok=True)
    out_name = f"{input_file.stem}.gcode.3mf"
    out_3mf = output_dir / out_name

    cmd = [str(bambu_studio)]
    if settings:
        cmd.extend(["--load-settings", settings])
    if filaments:
        cmd.extend(["--load-filaments", filaments])
    cmd.extend(["--slice", str(plate), "--outputdir", str(output_dir), "--export-3mf", out_name])
    if extra_args:
        cmd.extend(extra_args)
    cmd.append(str(input_file))

    print("スライス実行中:", " ".join(f'"{c}"' if " " in c else c for c in cmd))
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise RuntimeError(f"Bambu Studio のスライスに失敗しました (exit code: {result.returncode})")

    if out_3mf.exists():
        return out_3mf

    # Fallback: find generated 3mf in output_dir
    candidates = sorted(output_dir.glob("*.3mf"), key=lambda p: p.stat().st_mtime, reverse=True)
    if candidates:
        return candidates[0]

    raise FileNotFoundError(f"スライス後の .3mf ファイルが出力先に見つかりませんでした: {output_dir}")


def cmd_config(args: argparse.Namespace) -> int:
    cfg = load_config()
    updated = False

    if args.set_ip is not None:
        cfg["ip"] = args.set_ip
        updated = True
    if args.set_access_code is not None:
        cfg["access_code"] = args.set_access_code
        updated = True
    if args.set_serial is not None:
        cfg["serial"] = args.set_serial
        updated = True
    if args.bambu_studio is not None:
        cfg["bambu_studio_path"] = args.bambu_studio
        updated = True
    if args.default_settings is not None:
        cfg["default_settings"] = args.default_settings
        updated = True
    if args.default_filaments is not None:
        cfg["default_filaments"] = args.default_filaments
        updated = True

    if updated:
        save_config(cfg)
        print(f"設定を保存しました: {CONFIG_FILE}")

    masked = dict(cfg)
    if masked.get("access_code"):
        code = str(masked["access_code"])
        masked["access_code"] = code[:2] + "*" * max(0, len(code) - 2)

    print(json.dumps(masked, indent=2, ensure_ascii=False))
    return 0


def cmd_status(args: argparse.Namespace) -> int:
    cfg = load_config()
    ip, access_code, serial = resolve_credentials(args, cfg)
    printer = connect_mqtt(ip, access_code, serial, timeout=args.timeout)
    try:
        if args.json:
            print(json.dumps(printer.mqtt_dump(), indent=2, ensure_ascii=False, default=str))
            return 0

        info = {
            "state": str(printer.get_state()),
            "current_state": str(printer.get_current_state()),
            "file": printer.get_file_name() or printer.subtask_name(),
            "progress_pct": printer.get_percentage(),
            "remaining_min": printer.get_time(),
            "layer": f"{printer.current_layer_num()}/{printer.total_layer_num()}",
            "nozzle_temp_c": printer.get_nozzle_temperature(),
            "bed_temp_c": printer.get_bed_temperature(),
            "chamber_temp_c": printer.get_chamber_temperature(),
            "light": printer.get_light_state(),
            "wifi": printer.wifi_signal(),
        }
        for k, v in info.items():
            print(f"{k:16}: {v}")
        return 0
    finally:
        printer.mqtt_stop()


def cmd_slice(args: argparse.Namespace) -> int:
    cfg = load_config()
    bambu_studio = find_bambu_studio(cfg, args.bambu_studio)
    settings = args.settings or cfg.get("default_settings")
    filaments = args.filaments or cfg.get("default_filaments")
    output_dir = Path(args.output_dir) if args.output_dir else Path(args.file).resolve().parent

    out = run_slice(
        input_file=Path(args.file).resolve(),
        bambu_studio=bambu_studio,
        output_dir=output_dir,
        settings=settings,
        filaments=filaments,
        plate=args.plate,
    )
    print(f"スライス完了: {out}")
    return 0


def cmd_upload(args: argparse.Namespace) -> int:
    cfg = load_config()
    ip, access_code, serial = resolve_credentials(args, cfg)
    local_path = Path(args.file).resolve()
    if not local_path.exists():
        print(f"エラー: ファイルが見つかりません: {local_path}", file=sys.stderr)
        return 1

    remote_name = args.remote_name or local_path.name
    printer = bl.Printer(ip, access_code, serial)
    print(f"アップロード中: {local_path} -> {ip}:/{remote_name}")
    with local_path.open("rb") as f:
        res = printer.upload_file(f, remote_name)
    print(f"アップロード完了: {res}")
    return 0


def cmd_print(args: argparse.Namespace) -> int:
    cfg = load_config()
    ip, access_code, serial = resolve_credentials(args, cfg)

    target_path = Path(args.file).resolve()
    if not args.no_upload and not target_path.exists():
        print(f"エラー: ファイルが見つかりません: {target_path}", file=sys.stderr)
        return 1

    temp_dir: tempfile.TemporaryDirectory[str] | None = None
    try:
        needs_slice = args.slice or (
            not args.no_upload and target_path.suffix.lower() in {".stl", ".obj", ".step", ".stp"}
        )

        if needs_slice:
            bambu_studio = find_bambu_studio(cfg, args.bambu_studio)
            settings = args.settings or cfg.get("default_settings")
            filaments = args.filaments or cfg.get("default_filaments")
            temp_dir = tempfile.TemporaryDirectory(prefix="bambu_cli_")
            target_path = run_slice(
                input_file=target_path,
                bambu_studio=bambu_studio,
                output_dir=Path(temp_dir.name),
                settings=settings,
                filaments=filaments,
                plate=0,
            )
            print(f"スライス済みファイル: {target_path}")

        remote_name = args.remote_name or target_path.name

        printer = connect_mqtt(ip, access_code, serial, timeout=args.timeout)
        try:
            if not args.no_upload:
                print(f"アップロード中: {target_path.name} -> {ip}:/{remote_name}")
                with target_path.open("rb") as f:
                    upload_res = printer.upload_file(f, remote_name)
                print(f"アップロード完了: {upload_res}")

            ams_mapping = [int(x.strip()) for x in args.ams_mapping.split(",") if x.strip()]
            use_ams = not args.no_ams
            flow_cali = not args.no_flow_cali

            print(
                f"印刷開始指令を送信中: file={remote_name}, plate={args.plate}, "
                f"use_ams={use_ams}, ams_mapping={ams_mapping}, flow_calibration={flow_cali}"
            )
            ok = printer.start_print(
                filename=remote_name,
                plate_number=args.plate,
                use_ams=use_ams,
                ams_mapping=ams_mapping,
                flow_calibration=flow_cali,
            )
            time.sleep(1.5)
            if ok:
                print("印刷開始指令を送信しました。")
                return 0
            print("エラー: 印刷開始指令の送信に失敗しました。", file=sys.stderr)
            return 1
        finally:
            printer.mqtt_stop()
    finally:
        if temp_dir is not None:
            temp_dir.cleanup()


def cmd_control(args: argparse.Namespace) -> int:
    cfg = load_config()
    ip, access_code, serial = resolve_credentials(args, cfg)
    printer = connect_mqtt(ip, access_code, serial, timeout=args.timeout)
    try:
        action = args.command
        if action == "pause":
            ok = printer.pause_print()
        elif action == "resume":
            ok = printer.resume_print()
        elif action == "stop":
            ok = printer.stop_print()
        elif action == "light":
            ok = printer.turn_light_on() if args.state == "on" else printer.turn_light_off()
        elif action == "gcode":
            ok = printer.gcode(args.gcode_cmd)
        else:
            print(f"不明なコマンド: {action}", file=sys.stderr)
            return 1
        time.sleep(1.0)
        print(f"コマンド '{action}' 送信結果: {'OK' if ok else 'FAILED'}")
        return 0 if ok else 1
    finally:
        printer.mqtt_stop()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bambu-cli",
        description="Bambu Studio スライス & Bambu Lab プリンター LAN 印刷制御 CLI",
    )
    parser.add_argument("--ip", help="プリンターのIPアドレス (環境変数: BAMBU_IP)")
    parser.add_argument("--access-code", help="LANアクセスコード (環境変数: BAMBU_ACCESS_CODE)")
    parser.add_argument("--serial", help="プリンターのシリアル番号 (環境変数: BAMBU_SERIAL)")
    parser.add_argument("--timeout", type=float, default=10.0, help="MQTT接続タイムアウト秒 (デフォルト: 10)")

    sub = parser.add_subparsers(dest="command", required=True)

    # config
    p_cfg = sub.add_parser("config", help="接続情報やデフォルト設定の保存・表示")
    p_cfg.add_argument("--ip", dest="set_ip", help="プリンターのIPアドレスを保存")
    p_cfg.add_argument("--access-code", dest="set_access_code", help="LANアクセスコードを保存")
    p_cfg.add_argument("--serial", dest="set_serial", help="シリアル番号を保存")
    p_cfg.add_argument("--bambu-studio", help="bambu-studio.exe のパスを保存")
    p_cfg.add_argument("--default-settings", help="スライス時のデフォルト --load-settings 値 (machine.json;process.json)")
    p_cfg.add_argument("--default-filaments", help="スライス時のデフォルト --load-filaments 値")
    p_cfg.set_defaults(func=cmd_config)

    # status
    p_status = sub.add_parser("status", help="プリンターの現在の状態を表示")
    p_status.add_argument("--json", action="store_true", help="MQTT の生 JSON データを出力")
    p_status.set_defaults(func=cmd_status)

    # slice
    p_slice = sub.add_parser("slice", help="Bambu Studio CLI でモデルをスライス")
    p_slice.add_argument("file", help="入力ファイル (.stl / .3mf / .obj / .step)")
    p_slice.add_argument("--output-dir", "-o", help="出力先ディレクトリ")
    p_slice.add_argument("--settings", help="マシン/プロセス設定 JSON (セミコロン区切り)")
    p_slice.add_argument("--filaments", help="フィラメント設定 JSON (セミコロン区切り)")
    p_slice.add_argument("--plate", type=int, default=0, help="スライス対象プレート (0=全プレート)")
    p_slice.add_argument("--bambu-studio", help="bambu-studio.exe のパス")
    p_slice.set_defaults(func=cmd_slice)

    # upload
    p_up = sub.add_parser("upload", help="スライス済み .3mf ファイルをプリンターへ転送 (FTPS)")
    p_up.add_argument("file", help="アップロードするローカルファイル")
    p_up.add_argument("--remote-name", help="プリンター上のファイル名 (省略時は元ファイル名)")
    p_up.set_defaults(func=cmd_upload)

    # print
    p_print = sub.add_parser("print", help="ファイルをアップロードして印刷開始 (必要ならスライスも実行)")
    p_print.add_argument("file", help="印刷するファイル (.gcode.3mf / .3mf / .stl など)")
    p_print.add_argument("--plate", type=int, default=1, help="印刷するプレート番号 (デフォルト: 1)")
    p_print.add_argument("--remote-name", help="プリンター上のファイル名")
    p_print.add_argument("--no-upload", action="store_true", help="アップロードせずプリンター上の既存ファイルを印刷")
    p_print.add_argument("--no-ams", action="store_true", help="AMS を使用しない (外部スプール)")
    p_print.add_argument("--ams-mapping", default="0", help="AMS トレイマッピング (カンマ区切り、例: 0 または 0,1)")
    p_print.add_argument("--no-flow-cali", action="store_true", help="自動フローキャリブレーションを無効化")
    p_print.add_argument("--slice", action="store_true", help="印刷前に Bambu Studio CLI でスライスを実行")
    p_print.add_argument("--settings", help="スライス時の設定 JSON (セミコロン区切り)")
    p_print.add_argument("--filaments", help="スライス時のフィラメント設定 JSON")
    p_print.add_argument("--bambu-studio", help="bambu-studio.exe のパス")
    p_print.set_defaults(func=cmd_print)

    # pause / resume / stop
    for name, help_text in [
        ("pause", "印刷を一時停止"),
        ("resume", "一時停止中の印刷を再開"),
        ("stop", "印刷を中止"),
    ]:
        p_act = sub.add_parser(name, help=help_text)
        p_act.set_defaults(func=cmd_control)

    # light
    p_light = sub.add_parser("light", help="チャンバーライトの ON/OFF")
    p_light.add_argument("state", choices=["on", "off"], help="on または off")
    p_light.set_defaults(func=cmd_control)

    # gcode
    p_gc = sub.add_parser("gcode", help="任意の G-code コマンドを送信")
    p_gc.add_argument("gcode_cmd", help="送信する G-code 文字列 (例: \"G28\")")
    p_gc.set_defaults(func=cmd_control)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as exc:
        print(f"エラー: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
