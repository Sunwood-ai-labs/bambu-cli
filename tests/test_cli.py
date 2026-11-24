from __future__ import annotations

import json
from pathlib import Path
from unittest import mock

import pytest

from bambu_cli import cli


def test_build_parser_subcommands() -> None:
    parser = cli.build_parser()
    args = parser.parse_args(["config", "--ip", "192.168.1.50", "--access-code", "12345678", "--serial", "SN001"])
    assert args.command == "config"
    assert args.set_ip == "192.168.1.50"
    assert args.set_access_code == "12345678"
    assert args.set_serial == "SN001"


def test_config_saves_and_masks_access_code(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    cfg_dir = tmp_path / ".bambu-cli"
    cfg_file = cfg_dir / "config.json"
    with mock.patch.object(cli, "CONFIG_DIR", cfg_dir), mock.patch.object(cli, "CONFIG_FILE", cfg_file):
        rc = cli.main(["config", "--ip", "192.168.1.50", "--access-code", "12345678", "--serial", "SN001"])
        assert rc == 0
        saved = json.loads(cfg_file.read_text(encoding="utf-8"))
        assert saved["access_code"] == "12345678"

        out = capsys.readouterr().out
        assert "12******" in out
        assert "12345678" not in out


def test_resolve_credentials_priority(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("BAMBU_IP", "10.0.0.2")
    monkeypatch.setenv("BAMBU_ACCESS_CODE", "envcode")
    monkeypatch.setenv("BAMBU_SERIAL", "envserial")

    parser = cli.build_parser()
    args = parser.parse_args(["--ip", "10.0.0.9", "status"])
    ip, code, serial = cli.resolve_credentials(args, {"ip": "10.0.0.1", "access_code": "cfgcode", "serial": "cfgserial"})
    assert ip == "10.0.0.9"
    assert code == "envcode"
    assert serial == "envserial"


def test_print_parser_flags() -> None:
    parser = cli.build_parser()
    args = parser.parse_args(["print", "model.gcode.3mf", "--plate", "2", "--no-ams", "--no-flow-cali"])
    assert args.command == "print"
    assert args.file == "model.gcode.3mf"
    assert args.plate == 2
    assert args.no_ams is True
    assert args.no_flow_cali is True
