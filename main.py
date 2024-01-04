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
    print(f"{message.channel.id} {message.channel}message got")
    if message.author.bot:
        return
    
    if message.channel.id in CHANNEL:
        print("it is in channel")
        if message.attachments:
            print("message has attachment")
            for attachment in message.attachments:
                file = attachment
                spoiler = await file.to_file()
                spoiler.filename = f"SPOILER_{file.filename}"
                await message.channel.send(f"Send from: {message.author.display_name}", file=spoiler)
            await message.delete()

client.run(TOKEN)