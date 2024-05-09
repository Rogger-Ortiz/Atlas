import discord
from discord.ext import commands
import os
import asyncio

#Any extra libaries go under THIS LINE to import on live version

from pytube import YouTube as YT

defaultEmbedColor=discord.Color(0xb253d6)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)
errEmbed = discord.Embed(color=defaultEmbedColor)
queue = []

downloadPath = os.getenv("ATL_yt_downloadPath")

# Only The Campfire can execute these commands. Don't want to end up like Rhythm or Groovy.
def isNotCampfire(ctx):
    return ctx.guild.id not in [588386910951702550, 634782302068670494]

def play_next(ctx):
    if isNotCampfire(ctx):
        return
    voice = ctx.message.guild.voice_client
    if len(queue) > 0:
        url = queue.pop(0)
        yt = YT(url)
        stream = yt.streams.get_by_itag(251)
        stream.download(output_path=downloadPath,filename="audio.mp3")
        source = discord.FFmpegPCMAudio(downloadPath+"\\audio.mp3")
        player = voice.play(source, after=lambda e: play_next(ctx))

class YouTube(commands.Cog):
    description="Play any YouTube video in a voice channel, and control it using the below commands!"
    def __init__(self,bot):
        self.bot = bot

    
    @commands.command(name="play", help="Plays a song in a voice channel given a YouTube link!", usage="[url]")
    async def play(self, ctx, url=None):
        if isNotCampfire(ctx):
            print("Not campfire!")
            return
        if url==None or ("youtube.com" not in url and "youtu.be" not in url):
            await ctx.channel.send("Please enter a URL!")
            return
        
        try:
            queueEmbed = discord.Embed(color=defaultEmbedColor)
            voice = ctx.message.guild.voice_client
            if voice.is_playing():
                queue.append(url)
                queueEmbed.title="Video added to the queue!"
                queueEmbed.description="View using $queue"
                await ctx.send(embed=queueEmbed)
                return
        except:
            pass
        
        yt = YT(url)
        stream = yt.streams.get_by_itag(251)
        stream.download(output_path=downloadPath,filename="audio.mp3")
        source = discord.FFmpegPCMAudio(downloadPath+"\\audio.mp3")

        voice_client = discord.utils.get(ctx.bot.voice_clients, guild=ctx.message.guild)
        if voice_client == None:
            vc = await ctx.author.voice.channel.connect()
        else:
            vc = voice_client

        if ctx.author.voice.channel == None:    
            errEmbed.title="Not in a voice channel!"
            errEmbed.description="Please enter a voice channel before trying to play something!"
            await ctx.send(embed=errEmbed)
            return
        player = vc.play(source, after=lambda e: play_next(ctx))
        voice = ctx.message.guild.voice_client
        while voice.is_playing():
            await asyncio.sleep(90)
        os.remove(downloadPath+"\\audio.mp3")
        await voice.disconnect(force=True)

    @commands.command(name="dc", aliases=["disconnect"], help="Disconnects bot from voice channel")
    async def dc(self, ctx):
        if isNotCampfire(ctx):
            return
        voice = ctx.message.guild.voice_client
        if voice.is_playing():
            voice.stop()
        os.remove(downloadPath+"\\audio.mp3")
        await voice.disconnect(force=True)

    @commands.command(name="pause", help="Pauses the song that is currently playing")
    async def pause(self, ctx):
        if isNotCampfire(ctx):
            return
        voice = ctx.message.guild.voice_client
        if not voice.is_playing():
            await ctx.send("Can't pause what is not playing!")
            return
        voice.pause()

    @commands.command(name="resume", help="Resumes the song that is paused")
    async def resume(self, ctx):
        if isNotCampfire(ctx):
            return
        voice = ctx.message.guild.voice_client
        if not voice.is_paused():
            await ctx.send("Can't resume what is not paused!")
            return
        voice.resume()

    @commands.command(name="queue", help="Views the queue of songs to play")
    async def queue(self, ctx):
        if isNotCampfire(ctx):
            return
        voice = ctx.message.guild.voice_client
        queueEmbed=discord.Embed(color=defaultEmbedColor)
        if len(queue) == 0:
            queueEmbed.title="No songs in queue!"
            queueEmbed.description="Add songs to the queue using $play!"
            await ctx.send(embed=queueEmbed)
            return
        counter = 1
        qString = ""
        for url in queue:
            yt = YT(url)
            qString+=f"{counter}. **{yt.author}**\n{yt.title}\n\n"
        queueEmbed.title="Queue:"
        queueEmbed.description=qString
        await ctx.send(embed=queueEmbed)

    @commands.command(name="remove", help="Removes a song based on its queue position", usage="[queue number]")
    async def pop(self, ctx, num):
        if isNotCampfire(ctx):
            return
        popEmbed = discord.Embed(color=defaultEmbedColor)
        url = queue.pop(int(num)-1)
        title = YT(url).title
        author = YT(url).author
        popEmbed.title=f"Video removed from queue:"
        popEmbed.add_field(name=author, value=title)
        await ctx.send(embed=popEmbed)

    @commands.command(name="skip", help="Skips the current song, and plays the next in queue, if available")
    async def skip(self, ctx):
        if isNotCampfire(ctx):
            return
        skipEmbed = discord.Embed(color=defaultEmbedColor)
        voice = ctx.message.guild.voice_client
        if not voice.is_playing():
            skipEmbed.title="Not playing anything!"
            await ctx.send(embed=skipEmbed)
            return
        voice.stop()
        play_next(ctx)



async def setup(bot):
	await bot.add_cog(YouTube(bot))
