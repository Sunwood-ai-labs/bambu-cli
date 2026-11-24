# Command Reference

All commands accept global overrides: `--ip`, `--access-code`, `--serial`, and `--timeout`.

## `config`

Save or display connection settings and default Bambu Studio paths. Access codes are masked in printed output.

```powershell
bambu-cli config --ip 192.168.1.50 --access-code 12345678 --serial 01P00A000000000
bambu-cli config --bambu-studio "C:\path\to\bambu-studio.exe"
```

## `status`

Fetch real-time MQTT telemetry (`state`, `file`, `progress_pct`, `remaining_min`, `layer`, `nozzle_temp_c`, `bed_temp_c`, `chamber_temp_c`, `light`, `wifi`).

```powershell
bambu-cli status
bambu-cli status --json
```

## `slice`

Run Bambu Studio CLI headlessly to produce a `.gcode.3mf` file.

```powershell
bambu-cli slice .\model.stl --output-dir .\out --settings "machine.json;process.json" --filaments "filament.json"
```

## `upload`

Upload a sliced `.gcode.3mf` file over LAN FTPS (port `990`).

```powershell
bambu-cli upload .\model.gcode.3mf
```

## `print`

Upload (and optionally slice first) and trigger printing over MQTT (port `8883`).

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
