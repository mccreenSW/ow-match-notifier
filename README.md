
# Overwatch マッチング通知ツール
<img width="899" height="707" alt="image" src="https://github.com/user-attachments/assets/04a9c8c4-4897-4a65-9442-127821c2662a" />

Overwatch 2 の試合開始時の通信量の急増を検知し、Discord へ通知を送るツールです。
マッチング待機中に裏画面で作業や休憩をしている方に最適です。

## 🛠 機能
- **特定プロセス監視**: `Overwatch.exe` が使用している UDP ポートのみを狙い撃ちで監視します。
- **誤検知防止**: パケット数の閾値を設定でき、ブラウザ視聴などの他通信を無視します。
- **通知機能**: Discord Webhook を利用してスマホや PC に通知を飛ばします。
- **一時停止機能**: 検知後は Enter キーを押すまで監視を停止し、試合中の連投を防ぎます。

## 📋 準備
1. **Npcap のインストール**:
   パケット監視のために [Npcap](https://npcap.com/) のインストールが必要です。
   **※インストール時、必ず「Install Npcap in WinPcap API-compatible Mode」にチェックを入れてください。**
   [ダウンロードはこちら](https://npcap.com/dist/)
2. **PCの再起動**: インストール後、ドライバを有効にするため必ず再起動してください。
3. **Discord Webhook URL**:
   通知を送りたいチャンネルの Webhook URL を取得しておいてください。

## 🚀 使い方

### 1. 初回起動（設定ファイルの生成）
`overwatch_watch.exe` を実行してください。
初回起動時、exeと同じフォルダに `config.properties` が自動生成されます。

### 2. Webhookの設定
生成された `config.properties` をメモ帳などで開き、以下のように編集して保存します。
```ini
[Settings]
webhook_url = [https://discord.com/api/webhooks/xxxx](https://discord.com/api/webhooks/xxxx)...（あなたのURL）
packet_threshold = 150
```
※ packet_threshold（閾値）は、メニュー画面で誤検知する場合は数値を大きく（200〜300）調整してください。
```ini
3. 監視の開始
設定後、再度 overwatch_watch.exe を実行します。「監視開始」と表示されれば成功です。
マッチングを検知するとDiscordに通知が飛び、監視が一時停止します。

4. 監視の再開
試合が終わった後、次のマッチング待ちに入ったら、コマンドプロンプト画面で Enterキー を押してください。監視が再開されます。

⚠️ 注意事項
公認されているツールではないため、自己責任での利用をお願いします。
パケットを直接読み取るため、管理者権限で実行する仕様です。

Overwatch が起動していない状態ではポートを特定できないため、ゲームを起動してから実行することをお勧めします。


