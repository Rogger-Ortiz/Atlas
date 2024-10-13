
import discord
from discord.ext import commands
import platform
import os

defaultEmbedColor=discord.Color(0xb253d6)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)
checkmark = ":white_check_mark:"
xmark = ":x:"

# Check if I am the author
def RJisAuthor(ctx):
    return ctx.author.id == 248440677350899712

class debugging(commands.Cog):
    description=""
    def __init__(self,bot):
        self.bot = bot



    # Setup the debugging "Shutdown" command
    @commands.command(name="shutdown", hidden=True)
    async def shutdown(self, ctx):
        if RJisAuthor(ctx):
            # Quit
            await ctx.reply("byegood!")
            exit()
        else:
            return

    # Setup remote updating of the bot
    @commands.command(name="update", hidden=True)
    async def update(self, ctx):
         if RJisAuthor(ctx):
              if platform.system() == "Windows":
                   print("Can't update PTB this way!!!")
                   return
              if platform.system() == "Linux":
                   await ctx.reply("Updating, please allow me 5 seconds to reboot...")
                   print(f"### PID: {os.getpid()}")
                   os.system(f"./updateATL.sh {os.getpid()}")
                   exit()
         else:
              return
    
    @commands.command(name="ping", hidden=True)
    async def ping(self, ctx):
         if RJisAuthor(ctx):
              await ctx.reply("pong!!!")
              

async def setup(bot):
	await bot.add_cog(debugging(bot))
