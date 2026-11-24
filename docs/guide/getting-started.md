# Getting Started

`bambu-cli` bridges **Bambu Studio CLI** (headless slicing) and **`bambulabs-api`** (LAN FTPS file transfer + MQTT control) so you can slice and print on Bambu Lab printers from any terminal or AI agent.

## 1. Printer Prerequisites

On your Bambu Lab printer's touchscreen:

1. Enable **LAN Only Mode**.
2. Enable **Developer Mode** (required on recent firmware for third-party MQTT print control).
3. Record your **IP Address**, **Access Code**, and **Serial Number**.

## 2. Install `bambu-cli`

```bash
git clone https://github.com/Sunwood-ai-labs/bambu-cli.git
cd bambu-cli
uv pip install -e .
# or: pip install -e .
```

## 3. Configure Connection

```powershell
bambu-cli config --ip 192.168.1.50 --access-code 12345678 --serial 01P00A000000000
```

Settings are stored in `~/.bambu-cli/config.json`. You can also override them with `BAMBU_IP`, `BAMBU_ACCESS_CODE`, and `BAMBU_SERIAL`.

## 4. Verify & Print

```powershell
# Check live printer telemetry
bambu-cli status

# Upload and start a sliced .gcode.3mf
bambu-cli print .\model.gcode.3mf
```
