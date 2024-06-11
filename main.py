import discord
import datetime

TOKEN="DISCORD_BOT_TOKEN"
CHANNEL=[]
CHANNEL.append("CHANNEL_ID")
CHANNEL.append("CHANNEL_ID")

LOG_ROOM_CHANNEL = "LOG_ROOM_CHANNEL_ID"

intents = discord.Intents.all()
client = discord.Client(intents = intents)

@client.event
async def on_ready():
    print("ログイン成功")

@client.event
async def on_message(message):
    print(f"get message at {message.channel.id} {message.channel}")
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
                await message.channel.send(f"{message.content}", file=spoiler)
        
                logRoom = client.get_channel(LOG_ROOM_CHANNEL)
                log = await file.to_file()
                embed = discord.Embed(title = message.content)
                embed.add_field(name = "送信先", value = f"{message.guild.name} {message.channel.name}")
                embed.set_author(name = message.author.name,icon_url = message.author.avatar.url)
                embed.set_footer(text = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'))
                await logRoom.send(file=log, embed = embed)
            await message.delete()

client.run(TOKEN)
