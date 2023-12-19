import discord
from discord.ext import commands

defaultEmbedColor=discord.Color(0xe67e22)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)

class test(commands.Cog):
    description=""
    def __init__(self,bot):
        self.bot = bot

    # Print code here

async def setup(bot):
	await bot.add_cog(test(bot))
