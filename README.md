# make-ti-spoile
指定されたチャンネルに投稿された画像ファイルにスポイラーをかけるだけのbot


# 利用方法

## ライブラリのインストール
```bash
python -m pip install -r requirements.txt
```

## 定数の定義
main.py内の最初数行を編集する

```py
TOKEN="DISCORD_BOT_TOKEN" #DiscordBotのTokenを入力
CHANNEL=[]
CHANNEL.append("CHANNEL_ID") #自動スポイラーのチャンネルIDを入力
CHANNEL.append("CHANNEL_ID") #複数ある場合は入力、ない場合はこの行を削除

LOG_ROOM_CHANNEL = "LOG_ROOM_CHANNEL_ID" #動作ログを残すチャンネルのIDを入力
```

## 実行
```bash
python main.py
```
