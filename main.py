import discord

TOKEN="DISCORD_BOT_TOKEN"
CHANNEL=[]
CHANNEL.append("CHANNEL_ID")
CHANNEL.append("CHANNEL_ID")

intents = discord.Intents.all()
client = discord.Client(intents = intents)

@client.event
async def on_ready():
    print("ログイン成功")

@client.event
async def on_message(message):
    print("メッセージ検知")
    if message.author.bot:
        return
    
    if message.channel.id in CHANNEL:
        print(f"{message.channel.id} {message.channel}は該当します")
        if message.attachments:
            print("メッセージは添付ファイルを持ちます")
            for attachment in message.attachments:
                file = attachment
                file.filename = f"SPOILER_{file.filename}"
                spoiler = await file.to_file()
                await message.channel.send(file=spoiler)
            await message.delete()

client.run(TOKEN)