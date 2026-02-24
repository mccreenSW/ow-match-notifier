<img width="907" height="692" alt="aaa" src="https://github.com/user-attachments/assets/c2cf23da-b502-46bd-8957-c5f5c934aded" />

\# Overwatch マッチング通知ツール



Overwatch 2 の試合開始時の通信量の急増を検知し、Discord へ通知を送るツールです。

マッチング待機中に裏画面で作業や休憩をしている方に最適です。



\## 🛠 機能

\- \*\*特定プロセス監視\*\*: `Overwatch.exe` が使用している UDP ポートのみを狙い撃ちで監視します。

\- \*\*誤検知防止\*\*: パケット数の閾値を設定でき、ブラウザ視聴などの他通信を無視します。

\- \*\*通知機能\*\*: Discord Webhook を利用してスマホや PC に通知を飛ばします。

\- \*\*一時停止機能\*\*: 検知後は Enter キーを押すまで監視を停止し、試合中の連投を防ぎます。



\## 📋 準備

1\. \*\*Npcap のインストール\*\*:

&nbsp;  パケット監視のために \[Npcap](https://npcap.com/) のインストール（WinPcap互換モードにチェック）が必要です。（インストール後、再起動）

&nbsp;  https://npcap.com/dist/

2\. \*\*Discord Webhook URL\*\*:

&nbsp;  通知を送りたいチャンネルの Webhook URL を取得しておいてください。



\## 🚀 使い方

1\. `config.properties` を作成し、以下のように設定します。

&nbsp;  \[Settings]

&nbsp;  webhook\_url = YOUR\_DISCORD\_WEBHOOK\_URL

&nbsp;  packet\_threshold = 150





