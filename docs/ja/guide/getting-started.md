# はじめに

`bambu-cli` は、**Bambu Studio CLI**（ヘッドレススライス）と **`bambulabs-api`**（LAN FTPS 転送 + MQTT 制御）を組み合わせ、ターミナルや AI エージェントから直接 Bambu Lab プリンターを操作するためのツールです。

## 1. プリンター側の事前準備

プリンター本体のタッチパネルから以下を有効化してください：

1. **LAN Only Mode** を ON
2. **Developer Mode** を ON（※最新ファームウェアでサードパーティ CLI から MQTT 印刷指令を送るために必要）
3. 表示される **IPアドレス**・**アクセスコード（Access Code）**・**シリアル番号（Serial Number）** を控える

## 2. `bambu-cli` のインストール

```bash
git clone https://github.com/Sunwood-ai-labs/bambu-cli.git
cd bambu-cli
uv pip install -e .
# または: pip install -e .
```

## 3. 接続設定を保存

```powershell
bambu-cli config --ip 192.168.1.50 --access-code 12345678 --serial 01P00A000000000
```

設定は `~/.bambu-cli/config.json` に保存されます。環境変数（`BAMBU_IP`, `BAMBU_ACCESS_CODE`, `BAMBU_SERIAL`）での上書きも可能です。

## 4. ステータス確認 & 印刷開始

```powershell
# プリンターの実測テレメトリを確認
bambu-cli status

# スライス済み .gcode.3mf を転送して印刷開始
bambu-cli print .\model.gcode.3mf
```
