import discord
from discord.ext import commands
import json

defaultEmbedColor=discord.Color(0xb253d6)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)
checkmark = ":white_check_mark:"
xmark = ":x:"

#            "+"                   "Gaming n' Chill"   "Fantasy n' Chill"   "Shadowrealm"        "Raiding n' Chill"
whitelist = [1052076946210697256, 1063988726499381300, 1416604703243898961, 1419724821780234343, 1436378695169478830]

class VoiceChannel(commands.Cog):
    description = "Customize your custom VC name using:"
    def __init__(self,bot):
        self.bot = bot

    # Command to change either the "trigger channel" or set custom VC name
    @commands.command(name="vcname", help="Renames your custom voice Channel Name!", usage="[Channel Name]\n$vcname config [Channel ID](admins only)")
    async def vcname(self, ctx, name=None, config=None):

        # Return error if user does not supply name for custom VC
        if name == None:
            errorEmbed = discord.Embed(color=red, title="Please enter a name for your voice channel!", description="$vcname [Channel Name]")
            await ctx.reply(embed=errorEmbed)
            return
    
        # Return error if admin does not supply ID for trigger channel
        if name == "config":
            if not ctx.author.guild_permissions.administrator:
                errorEmbed = discord.Embed(color=red, title=f"{xmark} You cannot use that command!", description="Please contact an admin about using this command.")
                await ctx.reply(embed=errorEmbed)
                return
            if config == None:
                # Return error if no channel ID is supplied
                print(type(config))
                errorEmbed = discord.Embed(color=red, title="Please enter a valid Channel ID!", description="$vcname config [Channel ID]")
                await ctx.reply(embed=errorEmbed)
                return
            else:
                # Attempt to take supplied ID and turn into readable int. If we cant do it, send it back.
                try:
                    config = int(config)
                except:
                    errorEmbed = discord.Embed(color=red, title="Please enter a valid Channel ID!", description="$vcname config [Channel ID]")
                    await ctx.reply(embed=errorEmbed)
                    return
                
                # Make sure channel supplied is from this server
                channel = self.bot.get_guild(ctx.guild.id).get_channel(config)
                if channel == None:
                    errorEmbed = discord.Embed(color=red, title="Please enter an ID of a channel from this server!", description="$vcname config [Channel ID]")
                    await ctx.reply(embed=errorEmbed)
                    return
                
                # Set trigger channel after all checks pass
                with open("files/vcdata.json", "r") as readJson:
                    # Check if data exists. If not, make it.
                    vcData = json.load(readJson)
                    try:
                        vcData[str(ctx.guild.id)]["trigger"] = config
                    except:
                        vcData[str(ctx.guild.id)] = {"trigger": config, "active": {}}
                with open("files/vcdata.json", "w") as  writeJson: 
                    json.dump(vcData, writeJson)
                writeJson.close()
                readJson.close()
                successEmbed = discord.Embed(color=green, title=f"{checkmark} Trigger channel set to {channel.name}!", description="You can change this at any time.")
                await ctx.reply(embed=successEmbed)
                return
        
        # Change VC name if all above checks complete
        with open("files/vcdata.json", "r") as readJson:
            vcData = json.load(readJson)
            try:
                # Update name if applicable
                vcData[str(ctx.guild.id)][str(ctx.author.id)] = name
            except:
                # If no record trigger channel set, reject
                errorEmbed = discord.Embed(color=red, title=f"{xmark} No Trigger Channel set!", description="Ask an admin to run \"$vcname config [Channel ID]\" before setting any channel names!")
                await ctx.reply(embed=errorEmbed)
                return
        with open("files/vcdata.json", "w") as writeJson:
            json.dump(vcData, writeJson)
        writeJson.close()
        readJson.close()
        successEmbed = discord.Embed(color=green, title=f"{checkmark} Channel name set to \"{name}\" for {ctx.author.display_name}!")
        await ctx.reply(embed=successEmbed)
        return
    
    # Listen for when a user moves channels, and create if they join the trigger channel.
    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel is not None:
            # Check if they joined trigger channel
            with open("files/vcdata.json", "r") as readJson:
                vcData = json.load(readJson)
                if after.channel.id in [1052076946210697256, 1423041378559983678]:
                    # Move the user into their new VC, unless it exists, in which we move them to that VC instead.
                    guild = after.channel.guild
                    category = after.channel.category
                    active = after.channel.category.channels
                    try:
                        vcName = vcData[str(member.id)]
                    except:
                        vcName = member.display_name+"'s Channel"
                    # Try to move them there, if there is a disconnect in data, we will raise an exception.
                    try:
                        for channel in active:
                            if channel.name == vcName:
                                await member.move_to(channel)
                            else:
                                # In this case we must raise an exception to move to "except" clause
                                raise discord.DiscordException()
                    except:
                        # Create a new channel, move the user, and log it.
                        newChannel = await guild.create_voice_channel(vcName, category=category)
                        await member.move_to(newChannel)
            with open("files/vcdata.json", "w") as writeJson:
                json.dump(vcData, writeJson)
            writeJson.close()
            readJson.close()
            return

        if before.channel is not None:
            delete_vc = False
            if before.channel.id not in whitelist:    
                if before.channel.members == []:
                    delete_vc = True
            if delete_vc:
                await before.channel.delete()
            return

async def setup(bot):
	await bot.add_cog(VoiceChannel(bot))
