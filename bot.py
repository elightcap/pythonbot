import os
from typing import cast

import discord
import aiocron
from discord.ext import tasks, commands
from discord.utils import get
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNELID = os.getenv('DISCORD_CHANNEL')

client = discord.Client()
intents = discord.Intents.default()
intents.members = True
intents.messages=True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('Logged in as bot')
    print(client.user.name)
    print(client.user.id)
    print('------')

@aiocron.crontab('*/1 * * * *')
async def check_roles():
    channel = client.get_channel(CHANNELID)
    for member in client.get_all_members():
        if len(member.roles)<=1:
            messages = await channel.history(limit=200).flatten()
            for message in messages:
                memberRoles = member.roles
                if len(memberRoles)>=1:
                    await message.delete()
                

check_roles.start()
client.run(TOKEN)