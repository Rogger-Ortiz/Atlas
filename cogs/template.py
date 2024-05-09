import discord
from discord.ext import commands

defaultEmbedColor=discord.Color(0xb253d6)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)
checkmark = ":white_check_mark:"
xmark = ":x:"


class cogName(commands.Cog):
    description=""
    def __init__(self,bot):
        self.bot = bot

    # Print code here
        
async def setup(bot):
	await bot.add_cog(cogName(bot))
