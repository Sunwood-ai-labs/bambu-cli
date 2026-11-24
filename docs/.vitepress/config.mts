import { defineConfig } from 'vitepress'

export default defineConfig({
  title: 'bambu-cli',
  description: 'Headless Bambu Studio Slicing & LAN FTPS / MQTT Print Control CLI',
  base: '/bambu-cli/',
  cleanUrls: true,
  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/bambu-cli/icon.svg' }],
  ],
  themeConfig: {
    logo: '/icon.svg',
    socialLinks: [
      { icon: 'github', link: 'https://github.com/Sunwood-ai-labs/bambu-cli' },
    ],
    search: {
      provider: 'local',
    },
    footer: {
      message: 'Released under the MIT License.',
      copyright: 'Copyright © 2026 Sunwood AI Labs',
    },
  },
  locales: {
    root: {
      label: 'English',
      lang: 'en-US',
      themeConfig: {
        nav: [
          { text: 'Getting Started', link: '/guide/getting-started' },
          { text: 'Commands', link: '/guide/commands' },
          { text: 'Troubleshooting', link: '/guide/troubleshooting' },
        ],
        sidebar: [
          {
            text: 'Guide',
            items: [
              { text: 'Getting Started', link: '/guide/getting-started' },
              { text: 'Command Reference', link: '/guide/commands' },
              { text: 'Troubleshooting', link: '/guide/troubleshooting' },
            ],
          },
        ],
      },
    },
    ja: {
      label: '日本語',
      lang: 'ja-JP',
      link: '/ja/',
      title: 'bambu-cli',
      description: 'Bambu Studio CLI スライス & LAN FTPS / MQTT 印刷制御 CLI',
      themeConfig: {
        nav: [
          { text: 'はじめに', link: '/ja/guide/getting-started' },
          { text: 'コマンド一覧', link: '/ja/guide/commands' },
          { text: 'トラブルシュート', link: '/ja/guide/troubleshooting' },
        ],
        sidebar: [
          {
            text: 'ガイド',
            items: [
              { text: 'はじめに', link: '/ja/guide/getting-started' },
              { text: 'コマンド一覧', link: '/ja/guide/commands' },
              { text: 'トラブルシュート', link: '/ja/guide/troubleshooting' },
            ],
          },
        ],
      },
    },
  },
})
