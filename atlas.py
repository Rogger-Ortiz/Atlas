import os
import discord
from discord.ext import tasks, commands
import nest_asyncio
import asyncio

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='$', intents=intents)

# Removes help command so we can use our own
bot.remove_command('help')

# Define all of the cogs here (comment out what you won't use)
cogs = [
    'cogs.help',
    'cogs.vc',
    'cogs.debugging',
    'cogs.youtube',
    'cogs.moderation',
    'cogs.profile',
    #'cogs.test'
]

# Loads all of the cogs into the bot
async def loadall():
    for ext in cogs:
        await bot.load_extension(ext)

# Runs the function from before to load cogs
asyncio.run(loadall())

@bot.event
async def on_ready():
    # Start the status change every hour.
    profile = bot.get_cog("Profile")
    profile.changeStatus.start()

# Starts the bot (prod or dev)
bot.run(os.getenv("ATL_prod_key"))
#bot.run(os.getenv("ATL_dev_key"))