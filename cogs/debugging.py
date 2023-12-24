
import discord
from discord.ext import commands

defaultEmbedColor=discord.Color(0xe67e22)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)

class debugging(commands.Cog):
    description=""
    def __init__(self,bot):
        self.bot = bot

    # Setup the debugging "Shutdown" command
    @commands.command(name="shutdown", hidden=True)
    async def shutdown(self, ctx):
        # Make sure I (RJ) am the author
        if ctx.author.id != 248440677350899712:
            return
        else:
            # Quit
            await ctx.reply("Goodbye!")
            exit()

async def setup(bot):
	await bot.add_cog(debugging(bot))
