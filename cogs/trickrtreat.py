import discord
from discord.ext import commands
import os
from random import randint
from random import random
import asyncio
import json

#Any extra libaries go under THIS LINE to import on live version

defaultEmbedColor=discord.Color(0xe67e22)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)
trtDir = "/home/captain/boot/ATL/files/trt/"
#trtDir = "R:\\Projects\\Atlas\\files\\trt\\"
trtChance = 0.5

server_id = 588386910951702550
channel_id = 761019927170777108 
num_trt = 40

def bubbleSort(arr, arr2):
    n = len(arr)
    swapped = False
    for i in range(n-1):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                swapped = True
                arr[j], arr[j+1] = arr[j+1], arr[j]
                arr2[j], arr2[j+1] = arr2[j+1], arr2[j]
        if not swapped:
            return

# Drop Rates: 75%, 25%, 5%
item = [
        ["Space Trash","Silver Pants","Levitation Belt"],
        ["Assorted Bugs","Cool Geode","Tropical Flower"],
        ["Hairball","Toy Mouse","Can of Tuna"],
        ["Smushed Pumpkin","Spooky Lantern","Huge Hoof"],
        ["Goat Horns","Cherry Slushie","Wool Sweater"], #5
        ["Balloon Animal","Prank Flower","Clown Egg"],
        ["Broken Twigs","Cold Fries","Shiny Bauble"],
        ["Brimstone","Pitchfork","Inferno Hot Sauce"],
        ["Pixie Dust","Tiny Boots","Teeny Wand"],
        ["Swamp Gas","Lily Pad","Miniature Crown"], #10
        ["Drop of Ectoplasm","Rattlin' Chains","Mostly Finished Business"],
        ["Lucky Rock","Chewed Shoe","Half-Eaten Chocolate Bar"],
        ["Glitching Gizmo","Sparking Smartphone","Twitchy Tablet"],
        ["Eerie Acorn","Poison Apple","Evil Syrup"],
        ["Creepy Candle","Sinister Vine","Pumpkin's Ghost"], #15
        ["Bent Feather","Shiny Helmet","Enchanted Blade"],
        ["Wet Kelp"," Snorkel and Fins","Postcard from Atlantis"],
        ["Broken Lightbulb","Barn Owl Feathers","Blurry Photo"],
        ["Box of Bandages","Papyrus Scroll","Book of the Dead"],
        ["Roasted Seed","Hearty Soup","Perfect Pie"], #20
        ["Bowl of Orcslop","Wicked Dagger","Sweet Battleaxe"],
        ["Crusty Barnacle","Fearsome Eyepatch","Gold'n Doubloon"],
        ["Cough Drop","Fragrant Herbs","Gloomy Mask"],
        ["Tiny Crumbs","Fine CHeeseboard","Magic Flute"],
        ["Chilly CHess Piece","Souvenir Hourglass","Shivering Scythe"], #25
        ["Confusing Captchas","Positron Relay","Techno Mixtape"],
        ["Short Straw","Ragged Hat","Golden Corn"],
        ["Empty Test Tube","Tesla Coil","Shrink Ray"],
        ["Glass of Milk","Funny Bone","Grinning Skull"],
        ["Sour Jelly","Gourmet Jam","Prizewinning Preserves"], #30
        ["Baby Rattle","Feather Boa","Cool Eyepatch"],
        ["Cobwebs","Eight Tiny Shoes","Spidersilk Robe"],
        ["Spare Button","Bag of Rags","Picnic Basket"],
        ["Used Toothpick","Cape Coupon","Blood-Red Brooch"],
        ["Shedded Fur","Wolf Claw","Moonstone Pendant"], #35
        ["Eye of Newt","Toe of Frog","Witches' Brew"],
        ["Fossil Footprint","Corprolite","Meteorite Chunk"],
        ["Wumpling Soup","Wumpernickel Bread","Wumpkin Spice Latte"],
        ["Gnawed Bones","Snowball","Mountaineer's Hat"],
        ["Peabrain","Basic Brain","Galaxy Brain"], #40
        ]

class TrickRTreat(commands.Cog):
    description="Trick or Treat! For the month of October gather around and help answer the door for anyone who may stop by? And who knows, the most helpful may even receive somthing in return!"
    def __init__(self,bot):
        self.bot = bot

    # Print code here
    @commands.Cog.listener()
    async def on_message(self, msg):
        if msg.author.bot:
            return
        if msg.channel.id == channel_id:
            chance = random()
            #print(chance)
            if chance<trtChance:
                 trtEmbed = discord.Embed(color=defaultEmbedColor)
                 channel = self.bot.get_channel(channel_id)
                 filedir = os.listdir(f"{trtDir}")
                 filedir.sort()
                 trt = randint(0,1)
                 if trt == 0:
                     trt = "h$trick"
                 if trt == 1:
                     trt = "h$treat"
                 value = randint(0,39)
                 counter = 0
                 for file in filedir:
                     if counter == value:
                         item_gen = random()
                         item_val = 0
                         if item_gen < 1.0:
                             item_val = 0
                         if item_gen < 0.25:
                             item_val = 1
                         if item_gen < 0.05:
                             item_val = 2
                         item_str = item[value][item_val]
                         send_file = discord.File(f"{trtDir}{file}", filename=file)
                         trtEmbed.title = "Trick or Treat!"
                         trtEmbed.description = f"*Ding Dong*\n\nSomeone is at the door! Answer them using **{trt}**"
                         trtEmbed.set_footer(text="They won't wait forever! Answer them within the next minute to give them candy!")
                         trtEmbed.set_image(url=f'attachment://{file}')
                         break
                     else:
                         counter+=1
                 sent_message = await channel.send(file=send_file, embed=trtEmbed)
                 try:
                     message = await self.bot.wait_for('message', timeout=60.0, check=lambda message: trt in message.content)
                     successEmbed = discord.Embed(color=defaultEmbedColor)
                     successEmbed.set_image(url=f'attachment://{file}')
                     successEmbed.title = "Happy Halloween!"
                     successEmbed.description = f"As a thank you for your kindess, they give {message.author.mention} one **{item[value][item_val]}**"
                     if item_val == 0:
                         successEmbed.set_footer(text="This item is common. There's not much special about it. It has been added to your inventory.")
                     if item_val == 1:
                         successEmbed.set_footer(text="This item is uncommon. You take note of its existence. It has been added to your inventory.")
                     if item_val == 2:
                         successEmbed.set_footer(text="This item is rare!. Beaming with happiness, you add it to your inventory.") 
                     
                     memID = message.author.id
                     file = open(f'{trtDir}leaderboard.json', 'r+')
                     data = json.load(file)
                     try:
                         amt = data[str(memID)]
                         amt +=1
                         entry = f"{{\"{memID}\": {amt}}}"
                         newEntry = json.loads(entry)
                         data.update(newEntry)
                         file.truncate(0)
                         file.seek(0)
                         json.dump(data, file)
                         file.close()
                     except KeyError:
                         entry = f"{{\"{memID}\": 1}}"
                         newEntry = json.loads(entry)
                         data.update(newEntry)
                         file.truncate(0)
                         file.seek(0)
                         json.dump(data, file)
                         file.close()
    
                     await sent_message.edit(embed=successEmbed)
                 except asyncio.TimeoutError:
                     failEmbed = discord.Embed(color=defaultEmbedColor)
                     failEmbed.title = "The trick-or-treater disappeared..."
                     failEmbed.description = "No one noticed them and they left :("
                     await sent_message.edit(embed=failEmbed, attachments=[])

    @commands.command(aliases=["leaderbaord","lb"])
    async def leaderboard(self, ctx):
        file = open(f'{trtDir}leaderboard.json', 'r+')
        channel = ctx.channel
        data = json.load(file)
        user_str = []
        score = []
        lbEmbed = discord.Embed(color=defaultEmbedColor)
        for key in data:
            user_str.append(key)
            score.append(data[key])
        bubbleSort(score, user_str)
        score = score[::-1]
        user_str = user_str[::-1]
        #print(score)
        #print(user_str)
        lbStr = ""
        count = 0
        for i in range(len(user_str)):
            if(count>9):
                break
            uid = int(user_str[i])
            user_obj = self.bot.get_user(uid)
            score_num = score[i]
            lbStr+=f"{user_obj.mention}: {score_num}\n"
            count+=1
        lbEmbed.title = "Leaderboard"
        lbEmbed.description = lbStr
        lbEmbed.set_footer(text="Make sure to keep answering those doors!")
        await channel.send(embed=lbEmbed)
        





async def setup(bot):
	await bot.add_cog(TrickRTreat(bot))