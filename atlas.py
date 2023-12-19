import os
import discord
from discord.ext import tasks, commands
import nest_asyncio
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)

bot.run(os.getenv("ATL_key"))
