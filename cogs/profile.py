import discord
from discord.ext import commands, tasks
import random
from datetime import datetime

defaultEmbedColor=discord.Color(0xb253d6)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)
checkmark = ":white_check_mark:"
xmark = ":x:"
toggle = 0

twitch_link = "https://www.twitch.tv/xrj0"

# Set status of the bot, using a RNG and a match/case
async def setStatus(self):
    choice = random.randint(1,3)
    match choice:
        case 1:
            await self.bot.change_presence(activity=discord.Game(name="with the stars."))
        case 2:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="to the wind."))
        case 3:
            await self.bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="over all."))
    return


class Profile(commands.Cog):
    description="Messes with Atlas' internal profile settings"
    def __init__(self,bot):
        self.bot = bot
        # self.changeStatus.start()

    # Print code here
    @commands.command(name="streaming")
    async def streaming(self, ctx):
        global toggle
        # Only RJ can execute
        if ctx.author.id != 248440677350899712:
            return
        
        # If set to normal status, switch to hosting RJ stream
        if toggle == 0:
            await self.bot.change_presence(activity=discord.Streaming(name="RJ's livestream.", url=twitch_link))
            toggle = 1
            return
        
        # If set to RJ stream, turn off and return to normal status
        if toggle == 1:
            await setStatus(self)
            toggle = 0
            return
        
    # TODO - Run setStatus at the top of every hour
    @tasks.loop(hours=1.0)
    async def changeStatus(self):
        global toggle
        if toggle == 0:
            await setStatus(self)

async def setup(bot):
	await bot.add_cog(Profile(bot))
