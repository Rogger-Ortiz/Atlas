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
          with open("files\\moddata.json", "r") as readJson:
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
          with open("files\\moddata.json", "w") as writeJson:
               json.dump(modData, writeJson)
          writeJson.close()
          readJson.close()
      
     # Allow for admins to customize their own bad words
     @commands.command(name="badwords", aliases=["badword"], help="Adds or removes a bad word to add to moderation.\nA \"Full\" match matches standalone.\nA \"Partial\" match matches if the word appears in any substring of a message.", usage="[add/remove/list] [full/partial match](add/remove only) [word](add/remove only)")
     @has_permissions(administrator=True)
     async def badwords(self, ctx, setting=None, matchType=None, word=None):
          # Perform flag checks
          if setting == None or setting.lower() not in ["add", "remove", "list"]:
               errEmbed = discord.Embed(color=red, title=f"{xmark} Please use the correct flags!", description="Use \"$help badwords\" for syntax.")
               await ctx.reply(embed=errEmbed)
               return
          if setting.lower() in ["add", "remove"]:
               if matchType == None or matchType.lower() not in ["full", "partial"]:
                    errEmbed = discord.Embed(color=red, title=f"{xmark} Please use the correct flags!", description="Use \"$help badwords\" for syntax.")
                    await ctx.reply(embed=errEmbed)
                    return
          if setting.lower() in ["add", "remove"]:
               if matchType.lower() in ["full", "partial"]:
                    if word == None:
                         errEmbed = discord.Embed(color=red, title=f"{xmark} Please supply a word to add/remove!", description="Use \"$help badwords\" for syntax.")
                         await ctx.reply(embed=errEmbed)
                         return

          # Read the wordData for aleration
          wordData_raw = open("files\\badwords.json", "r")
          wordData = json.load(wordData_raw)
          wordData_raw.close()
          match setting:
               # Add word to the blacklist
               case "add":
                    try:
                         if word.lower() in wordData[str(ctx.guild.id)][matchType.lower()]:
                              errEmbed = discord.Embed(color=red, title=f"{xmark} Word already in blacklist!", description="Use \"$badwords list\" to view banned words")
                              await ctx.send(embed=errEmbed)
                              return
                         wordData[str(ctx.guild.id)][matchType.lower()].append(word)
                    except KeyError:
                         wordData[str(ctx.guild.id)] = {"full":[], "partial":[]}
                         wordData[str(ctx.guild.id)][matchType.lower()].append(word)
                    successEmbed = discord.Embed(color=green, title=f"{checkmark} Added word to blacklist!", description="Use \"$badwords list\" to view banned words")
                    await ctx.send(embed=successEmbed)
               # Remove word from the blacklist
               case "remove":
                    try:
                         wordData[str(ctx.guild.id)][matchType.lower()].remove(word.lower())
                    except KeyError:
                         errEmbed = discord.Embed(color=red, title=f"{xmark} Word is not moderated!", description="Use \"$help badwords\" for syntax.")
                         await ctx.reply(embed=errEmbed)
                    successEmbed = discord.Embed(color=green, title=f"{checkmark} Removed word from blacklist!", description="Use \"$badwords list\" to view banned words")
                    await ctx.send(embed=successEmbed)
               # List blacklist (privately, as to not lead to abuse of system)
               case "list":
                    listEmbed = discord.Embed(color=defaultEmbedColor, title=f"List of bad words for {ctx.guild.name}")
                    icon = ctx.guild.icon
                    if icon != None:
                         listEmbed.set_thumbnail(url=ctx.guild.icon.url)
                    fullString = ""
                    partialString = ""
                    try:
                         for word in wordData[str(ctx.guild.id)]["full"]:
                              fullString += word+"\n"
                    
                         for word in wordData[str(ctx.guild.id)]["partial"]:
                              partialString += word+"\n"
                         listEmbed.add_field(name="Full Matches", value=fullString, inline=True)
                         listEmbed.add_field(name="Partial Matches", value=partialString, inline=True)
                         await ctx.author.send(embed=listEmbed)
                    except:
                         errEmbed = discord.Embed(color=red, title=f"{xmark} No words moderated on server \"{ctx.guild.name}\"!")
                         await ctx.author.send(embed=errEmbed)
               # Default case
               case _:
                    errEmbed = discord.Embed(color=red, title=f"{xmark} Please use the correct flags!", description="Use \"$help badwords\" for syntax.")
                    await ctx.reply(embed=errEmbed)
                    return
          
          with open("files\\badwords.json", "w") as writeJson:
               json.dump(wordData, writeJson)
          writeJson.close()

 
     # Setting up listener for all messages sent EVERYWHERE
     @commands.Cog.listener()
     async def on_message(self, msg):
          # ignore any other bot's messages
          if msg.author.bot:
               return
          # administrators are not moderated
          if msg.author.guild_permissions.administrator:
               return
          
          # Check if the message contains bad word
          matchedWord = None
          badwords_json = open("files\\badwords.json", "r")
          badwords = json.load(badwords_json)
          badwords_json.close()
 
          message = msg.content.lower()
          try:
               partial = badwords[str(msg.guild.id)]["partial"]
               full = badwords[str(msg.guild.id)]["full"]
          except:
               return
          # Check if word is in any substring of message
          for word in partial:
                if word in message:
                     matchedWord = word
                     break
          
          # Check if standalone word was said
          for word in full:
               if word in message.split():
                     matchedWord = word
                     break
          
          # Actioning process
          modData = json.load(open("files\\moddata.json", "r"))
          if str(msg.guild.id) in modData:
               # Log if the server allows
               if "logging" in modData[str(msg.guild.id)]:
                    if modData[str(msg.guild.id)]["logging"] == "on":
                          if matchedWord == None:
                               return
 
                          # Build embed to return to user the details behind the censor
                          logEmbed = discord.Embed(color=defaultEmbedColor,
                                                   description=f"**Message sent by {msg.author.mention} deleted in {msg.channel.mention}**\nContent: \"{msg.content}\"")
                          logEmbed.add_field(name="Reason:", value="Banned Word", inline=True)
                          logEmbed.add_field(name="Specifically:", value=matchedWord, inline=True)
                          logEmbed.set_author(name=msg.author.display_name, icon_url=msg.author.display_avatar.url)
                          logEmbed.set_footer(text=f"Username: {msg.author.name} - Author ID: {msg.author.id}")
                          logChannel = self.bot.get_guild(msg.guild.id).get_channel(int(modData[str(msg.guild.id)]["channel"]))
                          await logChannel.send(embed=logEmbed)
               # Remove if the server allows
               if "toggle" in modData[str(msg.guild.id)]:
                    if modData[str(msg.guild.id)]["toggle"] == "on":
                          if matchedWord == None:
                               return
                          # Delete the message if the server wants.
                          await msg.delete()
 
               # Do nothing if not setup
               return

async def setup(bot):
	await bot.add_cog(Moderation(bot))
