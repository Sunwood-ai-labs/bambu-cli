# トラブルシューティング

## FTPS (`990`) は通るのに、MQTT (`8883`) がタイムアウトする

Bambu Lab A1 mini の MQTT (`8883`) は**同時接続できるクライアント数が非常に少ない**仕様です。別の PC などで Bambu Studio がプリンターに接続しっぱなしになっていると、FTPS (`990`) の転送は成功しても `status` や `print` などの MQTT 指令がタイムアウトします。

**対処法:**
1. 別の PC で開いている Bambu Studio を一度閉じる。
2. `bambu-cli status` を再実行する。
3. それでも復帰しない場合はプリンター本体を一度再起動する。

## Windows で管理者権限（UAC）なしで Bambu Studio を導入する

`winget` や通常インストーラーが UAC 昇格で止まる場合：

1. GitHub Releases から Bambu Studio の公式 Windows ZIP 版をダウンロードする。
2. ユーザー書き込み可能なフォルダ（例：`%LOCALAPPDATA%\Programs\Bambu Studio`）へ展開する。
3. `bambu-cli` に実行ファイルのパスを登録する：

```powershell
bambu-cli config --bambu-studio "$env:LOCALAPPDATA\Programs\Bambu Studio\bambu-studio.exe"
```
