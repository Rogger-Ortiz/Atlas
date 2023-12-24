import discord
from discord.ext import commands

defaultEmbedColor=discord.Color(0xe67e22)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)

class Moderation(commands.Cog):
    description=""
    def __init__(self,bot):
        self.bot = bot

    # Setting up listener for all messages sent EVERYWHERE
        # Grab default blacklisted words, as well as 

async def setup(bot):
	await bot.add_cog(Moderation(bot))
