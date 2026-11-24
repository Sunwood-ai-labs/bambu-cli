# Troubleshooting

## FTPS (`990`) succeeds, but MQTT (`8883`) times out

Bambu Lab A1 mini supports only a very limited number of concurrent MQTT (`8883`) connections. If another computer or Bambu Studio window is connected to the printer, CLI commands such as `status` or `print` can time out even while FTPS (`990`) uploads succeed.

**Resolution:**
1. Close Bambu Studio on other machines connected to the printer.
2. Retry `bambu-cli status`.
3. If the socket remains wedged, power-cycle the printer once.

## Installing Bambu Studio on Windows without UAC admin elevation

If `winget` or the standard MSI/EXE installer stalls on UAC prompts:

1. Download the official Windows ZIP release of Bambu Studio from GitHub Releases.
2. Extract it to a user-writable directory (e.g., `%LOCALAPPDATA%\Programs\Bambu Studio`).
3. Register the binary with `bambu-cli`:

```powershell
bambu-cli config --bambu-studio "$env:LOCALAPPDATA\Programs\Bambu Studio\bambu-studio.exe"
```
