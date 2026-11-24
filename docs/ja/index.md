---
layout: home

hero:
  name: "bambu-cli"
  text: "スライスから3D印刷開始までをターミナルで完結"
  tagline: "Bambu Studio CLI（ヘッドレススライス）と LAN FTPS (990) / MQTT (8883) 制御を一気通貫化する Bambu Lab 用 CLI。"
  image:
    src: /icon.svg
    alt: bambu-cli アイコン
  actions:
    - theme: brand
      text: はじめに
      link: /ja/guide/getting-started
    - theme: alt
      text: コマンド一覧
      link: /ja/guide/commands
    - theme: alt
      text: GitHub
      link: https://github.com/Sunwood-ai-labs/bambu-cli

features:
  - icon: ⚡
    title: スライス〜印刷開始を一気通貫
    details: .stl / .3mf / .gcode.3mf を受け取り、必要ならヘッドレススライス → FTPS (990) 転送 → MQTT (8883) 印刷開始を1コマンドで実行。
  - icon: 📊
    title: 実測テレメトリ & AIエージェント向け JSON
    details: 状態・進捗・レイヤー・ノズル/ベッド温度・Wi-Fi強度をリアルタイム取得。--json で生 MQTT ダンプにも対応。
  - icon: 🔒
    title: 認証情報のローカル分離
    details: IP・Access Code・Serial を ~/.bambu-cli/config.json に分離保存（表示時はマスク）。環境変数 BAMBU_* での上書きも対応。
---

<p align="center">
  <img src="/pipeline-card.png" alt="bambu-cli パイプライン構成図" style="border-radius: 12px; margin-top: 24px;" />
</p>
