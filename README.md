# bambu-cli

**Bambu Studio CLI（ヘッドレススライス）＋ `bambulabs-api`（LAN 経由 FTPS 転送 & MQTT 制御）を一気通貫にまとめた Bambu Lab 3D プリンター用 CLI ツール**です。

Bambu Studio 本体の CLI はスライス専用でネットワーク印刷指令には対応していないため、スライスからプリンターへの転送・印刷開始・温度や進捗の監視・一時停止/中止までをターミナルや AI エージェントから直接叩けるようにしています。

> Tested on **Bambu Lab A1 mini** (Windows / Bambu Studio `v02.09.01.70`, LAN Only Mode + Developer Mode).

---

## ✨ 特徴

- **ワンコマンドでスライス〜印刷開始**: `.stl` / `.3mf` / `.gcode.3mf` を受け取り、必要なら Bambu Studio CLI でスライス → FTPS (990) 転送 → MQTT (8883) で印刷開始
- **プリンター状態の実測取得**: `bambu-cli status` で状態 (`RUNNING` 等)・進捗・残り時間・レイヤー・ノズル/ベッド温度・Wi-Fi 強度を取得（`--json` で生 MQTT ダンプ対応）
- **印刷制御 & G-code 送信**: `pause` / `resume` / `stop` / `light on|off` / `gcode`
- **認証情報のローカル分離**: IP・Access Code・Serial は `~/.bambu-cli/config.json` に保存（環境変数 `BAMBU_IP` / `BAMBU_ACCESS_CODE` / `BAMBU_SERIAL` でも上書き可能）

---

## 📦 インストール

```bash
git clone https://github.com/Sunwood-ai-labs/bambu-cli.git
cd bambu-cli
pip install -e .
```

※スライス機能を使う場合は [Bambu Studio](https://github.com/bambulab/BambuStudio/releases) が必要です（Windows で管理者権限/UAC を使わず入れたい場合は、GitHub Releases の Windows ZIP 版を展開して `bambu-cli config --bambu-studio <パス>` で指定できます）。

---

## 🔧 事前準備（プリンター本体側）

プリンター本体のタッチパネルから以下を有効化してください：

1. **LAN Only Mode** を ON
2. **Developer Mode** を ON（※最新ファームウェアでサードパーティ CLI から MQTT 印刷指令を送るために必要）
3. 画面に表示される **IPアドレス**・**アクセスコード（Access Code）**・**シリアル番号（Serial Number）** を控える

---

## 🚀 クイックスタート（3ステップ）

### 1. 接続設定を保存

```powershell
bambu-cli config --ip 192.168.1.50 --access-code 12345678 --serial 01P00A000000000
```

### 2. 接続・ステータス確認

```powershell
bambu-cli status
```

### 3. 転送＆印刷開始（またはスライス付き印刷）

```powershell
# スライス済み .gcode.3mf を転送して印刷開始
bambu-cli print .\model.gcode.3mf

# AMS を使わず外部スプールで印刷
bambu-cli print .\model.gcode.3mf --no-ams

# STL を Bambu Studio CLI でスライスしてからそのまま印刷
bambu-cli print .\model.stl --settings "machine.json;process.json" --filaments "filament.json"
```

---

## 🛠️ その他のコマンド

```powershell
# スライスのみ実行
bambu-cli slice .\model.stl --output-dir .\out

# FTPS アップロードのみ実行
bambu-cli upload .\model.gcode.3mf

# 印刷の一時停止 / 再開 / 中止
bambu-cli pause
bambu-cli resume
bambu-cli stop

# チャンバーライト操作
bambu-cli light on
bambu-cli light off

# 生 MQTT JSON ダンプ（エージェント連携・デバッグ用）
bambu-cli status --json
```

---

## ⚠️ 実戦トラブルシュート（ハマりポイント）

### FTPS（ポート 990）は繋がるのに、MQTT（ポート 8883）がタイムアウトする
Bambu Lab A1 mini の MQTT（8883）は**同時接続できるクライアント数が非常に少ない**仕様です。
別の PC やスマホで Bambu Studio などがプリンターに接続しっぱなしになっていると、CLI 側の `status` や `print` がタイムアウトします。

- **対処法**: 別 PC の Bambu Studio を一度閉じてから `bambu-cli` を実行してください（それでも復帰しない場合はプリンター本体を再起動）。

---

## 📄 License

MIT License — see [LICENSE](./LICENSE).
