import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import json

defaultEmbedColor=discord.Color(0xb253d6)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)
checkmark = ":white_check_mark:"
xmark = ":x:"

class Moderation(commands.Cog):
    description="Toggle the in-house moderation (beta) and configure the log channel"
    def __init__(self,bot):
        self.bot = bot

    # Allow for toggle of moderation
    @commands.command(name="moderation", aliases=["moderate"], help="Toggle moderation, as well as configure which channel to log in.", usage="[toggle/logging] [on/off] [channel id](logging only)")
    @has_permissions(administrator=True)
    async def moderation(self, ctx, setting=None, switch=None, channelID=None):
         successEmbed = discord.Embed(color=green, title="")
         with open("files\moddata.json", "r") as readJson:
              modData = json.load(readJson)
              match setting:
                   # Toggle the moderation on/off
                   case "toggle":
                        if switch == "on":
                             try:
                                  modData[str(ctx.guild.id)]["toggle"] = "on"
                             except KeyError:
                                  modData[str(ctx.guild.id)] = {"toggle":"on"}
                             successEmbed.title = f"{checkmark} Moderation toggled on!"

                        if switch == "off":
                             try:
                                  modData[str(ctx.guild.id)]["toggle"] = "off"
                             except KeyError:
                                  modData[str(ctx.guild.id)] = {"toggle":"off"}
                             successEmbed.title = f"{checkmark} Moderation toggled off!"
                        await ctx.reply(embed=successEmbed)
                   
                   case "logging":
                        if switch == "on":
                             # Make sure all the requried flags are sent and verify that they are correct.
                             if channelID == None or self.bot.get_guild(ctx.guild.id).get_channel(int(channelID)) == None or not isinstance(self.bot.get_guild(ctx.guild.id).get_channel(int(channelID)), discord.TextChannel):
                                   errEmbed = discord.Embed(color=red, title=f"{xmark} Please supply a text channel ID with that request", description="Use \"$help moderation\" for syntax.")
                                   await ctx.reply(embed=errEmbed)
                                   readJson.close()
                                   return
                             # Turn the logging on
                             try:
                                  modData[str(ctx.guild.id)]["logging"] = "on"
                                  modData[str(ctx.guild.id)]["channel"] = int(channelID)
                             except KeyError:
                                  modData[str(ctx.guild.id)] = {"logging":"on", "channel":int(channelID)}
                             successEmbed.title = f"{checkmark} Logging toggled on!"

                        if switch == "off":
                             # Turn the logging off
                             try:
                                  modData[str(ctx.guild.id)]["logging"] = "off"
                                  modData[str(ctx.guild.id)]["channel"] = None
                             except KeyError:
                                  modData[str(ctx.guild.id)] = {"logging":"off", "channel":None}
                             successEmbed.title = f"{checkmark} Logging toggled off!"
                        await ctx.reply(embed=successEmbed)

                   # Default handle case
                   case _:
                        errEmbed = discord.Embed(color=red, title=f"{xmark} Please use the correct flags!", description="Use \"$help moderation\" for syntax.")
                        await ctx.reply(embed=errEmbed)
                        readJson.close()
                        return
         with open("files\moddata.json", "w") as writeJson:
              json.dump(modData, writeJson)
         writeJson.close()
         readJson.close()

    # Setting up listener for all messages sent EVERYWHERE
    @commands.Cog.listener()
    async def on_message(self, msg):
         # ignore any other bot's messages
         if msg.author.bot:
              return
         
         modData = json.load(open("files\moddata.json", "r"))
         if str(msg.guild.id) in modData:
              if "logging" in modData[str(msg.guild.id)]:
                   if modData[str(msg.guild.id)]["logging"] == "on":
                         matchedWord = None
                         # TODO - filter words in message to check if naughty
                         badwords_json = open("files\\badwords.json", "r")
                         badwords = json.load(badwords_json)
                         badwords_json.close()

                         message = msg.content.lower()
                         partial = badwords["Partial"]
                         full = badwords["Full"]
                         for word in partial:
                              if word in message:
                                   matchedWord = word
                                   break

                         for word in full:
                              if word in message.split():
                                   matchedWord = word
                                   break
                         
                         if matchedWord == None:
                              return

                         # Build embed to return to user the details behind the censor
                         logEmbed = discord.Embed(color=defaultEmbedColor,
                                                  description=f"**Message sent by {msg.author.mention} deleted in {msg.channel.mention}**\nContent: \"{msg.content}\"")
                         logEmbed.add_field(name="Reason:", value="Banned Word", inline=True)
                         logEmbed.add_field(name="Specifically:", value=matchedWord, inline=True)
                         logEmbed.set_author(name=msg.author.name, icon_url=msg.author.avatar.url)
                         logEmbed.set_footer(text=f"Author ID: {msg.author.id} - Message ID: {msg.id}")
                         logChannel = self.bot.get_guild(msg.guild.id).get_channel(int(modData[str(msg.guild.id)]["channel"]))
                         await logChannel.send(embed=logEmbed)
                         print("Log it")

              if "toggle" in modData[str(msg.guild.id)]:
                   if modData[str(msg.guild.id)]["toggle"] == "on":
                         # Delete the message if the server wants.
                         await msg.delete()

              return

async def setup(bot):
	await bot.add_cog(Moderation(bot))
