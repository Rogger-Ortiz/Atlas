import discord
from discord.ext import commands

defaultEmbedColor=discord.Color(0xb253d6)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)
checkmark = ":white_check_mark:"
xmark = ":x:"

#Any extra libaries go under THIS LINE to import on live version


class Help(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    # Print code here
    @commands.command(name="help", help="Shows this message")
    async def MyHelpCommand(self, ctx, arg=None):
        defaultEmbedColor=discord.Color(0xe67e22)
        if arg==None:
            helpEmbed = discord.Embed(title='Help', description="List of commands:", color=defaultEmbedColor)
            helpEmbed.set_author(name=self.bot.user.display_name, icon_url=self.bot.user.display_avatar.url)
            helpEmbed.set_footer(text="** Get details on each command using $help [command]! **")
            for cog in self.bot.cogs:
                cog = self.bot.get_cog(cog)
                if cog.qualified_name != "Help":
                    name = "__"+cog.qualified_name+"__- *"+cog.description+"*"
                    value = ""
                    for command in cog.get_commands():
                        if not command.hidden:
                            value += f"**${command.name}**: {command.help}\n"
                    if name != "____" and value != "":
                        helpEmbed.add_field(name=name, value=value, inline=False)
            await ctx.reply(embed=helpEmbed)
        else:
            cmd = str(arg)
            command = self.bot.get_command(cmd)
            if command == None:
                errorEmbed = discord.Embed(color=0xFF0000, description=f":x: Command \"{cmd}\" not found!")
                await ctx.reply(embed=errorEmbed)
            cmdEmbed = discord.Embed(color=defaultEmbedColor, title=f"${command.name} {command.usage}", description=command.help)
            await ctx.reply(embed=cmdEmbed)


async def setup(bot):
	await bot.add_cog(Help(bot))
