import discord
from discord import app_commands
import datetime

import json
import os

CONFIG_FILE = "config.json"

config = {
    "DISCORD_BOT_TOKEN": "DISCORD_BOT_TOKEN",
    "CHANNEL": [
        "CHANNEL_ID",
        "CHANNEL_ID"
    ],
    "LOG_ROOM_CHANNEL": "LOG_ROOM_CHANNEL_ID"
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    else:
        return None

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=4)

def initialize():
    
    print("初期化完了")

config = load_config()

intents = discord.Intents.all()
client = discord.Client(intents = intents)

commandTree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print("ログイン成功")
    initialize()
    for i in client.guilds:
        commandTree.clear_commands(guild = discord.Object(id = i.id))
    await commandTree.sync()

@client.event
async def on_message(message):
    print(f"get message at {message.channel.id} {message.channel}")
    if message.author.bot:
        return
    
    if message.channel.id in config["CHANNEL"]:
        print("it is in channel")
        if message.attachments:
            print("message has attachment")
            for attachment in message.attachments:
                file = attachment
                
                spoiler = await file.to_file()
                spoiler.filename = f"SPOILER_{file.filename}"
                spomsg = await message.channel.send(f"{message.content}", file=spoiler)
                
                await spomsg.add_reaction("⬇")
                await spomsg.add_reaction("⬆")
                
                sendLog(message, file)
        else:
            print("message has no attachment")
            spomsg = await message.channel.send(f"{message.content}")
            
            await spomsg.add_reaction("⬇")
            await spomsg.add_reaction("⬆")
            
            sendLog(message)
        await message.delete()

def sendLog(message, file = None):
    log = None
    if file is not None:
        file.to_file()
        log = file
    logRoom = client.get_channel(config["LOG_ROOM_CHANNEL"])
    embed = discord.Embed(title = message.content)
    embed.add_field(name = "送信先", value = f"{message.guild.name} {message.channel.name}")
    embed.set_author(name = message.author.name,icon_url = message.author.avatar.url)
    embed.set_footer(text = datetime.datetime.now().strftime('%Y年%m月%d日 %H:%M:%S'))
    logRoom.send(file=log, embed = embed)

@commandTree.command(name="addchannel", description="スポイラーにするチャンネルを追加")
async def control_command(interaction: discord.Interaction):
    view = addChannelView()
    
    await interaction.response.send_message(view=view, content="チャンネルを選択してください")

class addChannelView(discord.ui.View):
    @discord.ui.select(cls=discord.ui.ChannelSelect, channel_types=[discord.ChannelType.text], placeholder="チャンネルを選択してください", min_values=1)
    async def selectMenu(self, interaction: discord.Interaction, select: discord.ui.ChannelSelect):
        config["CHANNEL"].append(select.values[0].id)
        save_config(config)
        await interaction.response.send_message(f"{select.values[0]}を追加しました")

@commandTree.command(name="removechannel", description="スポイラーにするチャンネルを削除")
async def control_command(interaction: discord.Interaction):
    view = removeChannelView()
    
    await interaction.response.send_message(view=view, content="チャンネルを選択してください")
    
class removeChannelView(discord.ui.View):
    @discord.ui.select(cls=discord.ui.ChannelSelect, channel_types=[discord.ChannelType.text], placeholder="チャンネルを選択してください", min_values=1)
    async def selectMenu(self, interaction: discord.Interaction, select: discord.ui.ChannelSelect):
        config["CHANNEL"].remove(select.values[0].id)
        save_config(config)
        await interaction.response.send_message(f"{select.values[0]}を削除しました")



client.run(config["DISCORD_BOT_TOKEN"])