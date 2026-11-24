---
layout: home

hero:
  name: "bambu-cli"
  text: "Slice, Transfer & Print from the Terminal"
  tagline: "Headless Bambu Studio CLI slicing combined with LAN FTPS (990) & MQTT (8883) print control for Bambu Lab 3D printers."
  image:
    src: /icon.svg
    alt: bambu-cli icon
  actions:
    - theme: brand
      text: Getting Started
      link: /guide/getting-started
    - theme: alt
      text: Command Reference
      link: /guide/commands
    - theme: alt
      text: GitHub
      link: https://github.com/Sunwood-ai-labs/bambu-cli

features:
  - icon: ⚡
    title: End-to-End Slice-to-Print
    details: Pass .stl, .3mf, or .gcode.3mf to slice headlessly, upload via FTPS (990), and trigger printing via MQTT (8883) in one command.
  - icon: 📊
    title: Live Telemetry & Agent JSON
    details: Query live state, layer progress, nozzle/bed temperatures, and Wi-Fi signal with human-readable output or raw --json MQTT dumps.
  - icon: 🔒
    title: Local Credential Isolation
    details: Saves IP, Access Code, and Serial to ~/.bambu-cli/config.json with masked output and BAMBU_* environment variable overrides.
---

<p align="center">
  <img src="/pipeline-card.png" alt="bambu-cli pipeline overview" style="border-radius: 12px; margin-top: 24px;" />
</p>
