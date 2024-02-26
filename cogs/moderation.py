import discord
from discord.ext import commands
import json

defaultEmbedColor=discord.Color(0xe67e22)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)
checkmark = ":white_check_mark:"
xmark = ":x:"

async def remove_and_log(self, modData, msg):
    author = msg.author.name
    avatar = msg.author.display_avatar.url
    authid = msg.author.id
    await msg.delete()
    try:
        channel=self.bot.get_channel(modData["modlog"])
        censorEmbed = discord.Embed(color=defaultEmbedColor, description=f"**Message sent by {msg.author.mention} deleted in {msg.channel.mention}**\n{message}")
        censorEmbed.set_author(name=author, icon_url=avatar)
        censorEmbed.add_field(name="Reason",value="Banned Word",inline=True)
        censorEmbed.add_field(name="Specifically:",value=word)
        censorEmbed.set_footer(text="ID: "+str(authid))
        await channel.send(embed=censorEmbed)
    except:
        pass

class Moderation(commands.Cog):
    description=""
    def __init__(self,bot):
        self.bot = bot

    # Allow for customization of moderation
    @commands.command(name="moderation", help="Toggle moderation, as well as add any extra terms to ignore (off by default)", usage="[On/Off/Add/Remove] [Term to add/remove] [partial/exact]")
    async def moderation(self, ctx, flag=None, term=None, detection=None):
        match flag.lower():
            case "on":
                # Add server ID to data[servers2mod]
                with open("files\\moderate.json", "r") as readData:
                    modData = json.load(data)
                    modData[str(ctx.guild.id)] = {}
                with open("files\\moderate.json", "r") as writeData:
                    json.dump(modData, writeData)
                readData.close()
                writeData.close()
                    
            case "off":
                # Remove server ID from data[servers2mod]
                with open("files\\moderate.json", "r") as readData:
                    modData = json.load(data)
                    try:
                        modData.pop(ctx.guild.id)
                    except ValueError:
                        pass
                with open("files\\moderate.json", "w") as writeData:
                    json.dump(modData)
                readData.close()
                writeData.close()

            case "add":
                # Verify flags are set properly
                if term == None or detection.lower() != "partial" or detection.lower() != "exact":
                    await ctx.reply("One or more flags were not set properly, please use \"$help moderation\" if you need help!")
                
                # Add word to array of no-no words
                with open("files\\moderate.json") as data:
                    modData = json.load(data)
                    modData[ctx.guild.id]

            case "remove":
                # Verify flags are set properly
                if term == None or detection.lower() != "partial" or detection.lower() != "exact":
                    await ctx.reply("One or more flags were not set properly, please use \"$help moderation\" if you need help!")
         

    # Allow users to setup channel to log moderation
    @commands.command(name="modlog", help="Set a channel to log moderation", usage="[Channel ID]")
    async def modlog(self, ctx, channel=None):
        return      

    # Setting up listener for all messages sent EVERYWHERE
    @commands.Cog.listener()
    async def on_message(self, msg):
         # ignore any other bot's messages
         if msg.author.bot:
              return
         
         # Grab default blacklisted words per server and check if server needs to be moderated
         with open(file="files\\moderate.json") as blist:
            modData = json.load(blist)
            if msg.channel.guild.id not in modData["servers2mod"]:
                return
            try:
                badWords = modData[msg.channel.guild.id]
            except KeyError:
                print("Server not moderated")
                return
            # First run through all the partial matches to be found
            partialMatch = badWords["partial"]
            for word in partialMatch:
                if word in msg:
                    # Remove msg and log it in modlog if applicable
                    await remove_and_log(self, modData, msg)

            # Now we run through all the whole matches to be found
            fullMatch = badWords["full"]
            wordList = msg.split()
            for word in fullMatch:
                if word in wordList:
                    await remove_and_log(self, modData, msg)

async def setup(bot):
	await bot.add_cog(Moderation(bot))
