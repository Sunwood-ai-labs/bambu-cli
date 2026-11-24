# コマンド一覧

すべてのコマンドで `--ip`, `--access-code`, `--serial`, `--timeout` のグローバル上書きが可能です。

## `config`

接続情報や Bambu Studio のデフォルトパスを保存・表示します（表示時は Access Code をマスク）。

```powershell
bambu-cli config --ip 192.168.1.50 --access-code 12345678 --serial 01P00A000000000
bambu-cli config --bambu-studio "C:\path\to\bambu-studio.exe"
```

## `status`

MQTT からリアルタイムのテレメトリ（`state`, `file`, `progress_pct`, `remaining_min`, `layer`, `nozzle_temp_c`, `bed_temp_c`, `chamber_temp_c`, `light`, `wifi`）を取得します。

```powershell
bambu-cli status
bambu-cli status --json
```

## `slice`

Bambu Studio CLI をヘッドレス実行して `.gcode.3mf` を生成します。

```powershell
bambu-cli slice .\model.stl --output-dir .\out --settings "machine.json;process.json" --filaments "filament.json"
```

## `upload`

スライス済み `.gcode.3mf` を LAN FTPS（ポート `990`）でプリンターへ転送します。

```powershell
bambu-cli upload .\model.gcode.3mf
```

## `print`

必要に応じてスライスを行い、FTPS 転送した上で MQTT（ポート `8883`）から印刷を開始します。

```powershell
bambu-cli print .\model.gcode.3mf
bambu-cli print .\model.gcode.3mf --no-ams
bambu-cli print .\model.stl --slice --settings "machine.json;process.json" --filaments "filament.json"
```

## `pause` / `resume` / `stop` / `light` / `gcode`

```powershell
bambu-cli pause
bambu-cli resume
bambu-cli stop
bambu-cli light on
bambu-cli light off
bambu-cli gcode "G28"
```
