import discord
from discord.ext import commands

defaultEmbedColor=discord.Color(0xb253d6)
green = discord.Color(0x00FF00)
red = discord.Color(0xFF0000)
checkmark = ":white_check_mark:"
xmark = ":x:"

current_bis = {
     "pld":"https://www.thebalanceffxiv.com/jobs/tanks/paladin/best-in-slot",
     "war":"https://www.thebalanceffxiv.com/jobs/tanks/warrior/best-in-slot",
     "drk":"https://www.thebalanceffxiv.com/jobs/tanks/dark-knight/best-in-slot",
     "gnb":"https://www.thebalanceffxiv.com/jobs/tanks/gunbreaker/best-in-slot",
     "whm":"https://www.thebalanceffxiv.com/jobs/healers/white-mage/best-in-slot",
     "sch":"https://www.thebalanceffxiv.com/jobs/healers/scholar/best-in-slot",
     "ast":"https://www.thebalanceffxiv.com/jobs/healers/astrologian/best-in-slot",
     "sge":"https://www.thebalanceffxiv.com/jobs/healers/sage/best-in-slot",
     "mnk":"https://www.thebalanceffxiv.com/jobs/melee/monk/best-in-slot",
     "drg":"https://www.thebalanceffxiv.com/jobs/melee/dragoon/best-in-slot",
     "nin":"https://www.thebalanceffxiv.com/jobs/melee/ninja/best-in-slot",
     "sam":"https://www.thebalanceffxiv.com/jobs/melee/samurai/best-in-slot",
     "rpr":"https://www.thebalanceffxiv.com/jobs/melee/reaper/best-in-slot",
     "vpr":"https://www.thebalanceffxiv.com/jobs/melee/viper/best-in-slot",
     "brd":"https://www.thebalanceffxiv.com/jobs/ranged/bard/best-in-slot",
     "mch":"https://www.thebalanceffxiv.com/jobs/ranged/machinist/best-in-slot",
     "dnc":"https://www.thebalanceffxiv.com/jobs/ranged/dancer/best-in-slot",
     "blm":"https://www.thebalanceffxiv.com/jobs/casters/black-mage/best-in-slot",
     "rdm":"https://www.thebalanceffxiv.com/jobs/casters/red-mage/best-in-slot",
     "smn":"https://www.thebalanceffxiv.com/jobs/casters/summoner/best-in-slot",
     "pct":"https://www.thebalanceffxiv.com/jobs/casters/pictomancer/best-in-slot"
}

fru_bis = {
     "pld":"https://xivgear.app/?page=bis|pld|ultimate|fru",
     "war":"https://xivgear.app/#/bis/war/ultimate/fru",
     "drk":"https://xivgear.app/#/bis/drk/ultimate/fru",
     "gnb":"https://xivgear.app/#/bis/gnb/ultimates/fru",
     "whm":"https://xivgear.app/?page=sl%7C4be4a46c-b60c-4b48-8380-a9329febdce0",
     "sch":"https://xivgear.app/?page=sl|acaa72cf-882b-4817-a211-267ce2268c1b",
     "ast":"https://xivgear.app/?page=sl|3ddfd0c8-c6e0-4856-9e5f-e064687fc88a",
     "sge":"https://xivgear.app/?page=sl|f5d6235f-4517-4328-9cb5-370d9d3c931f",
     "mnk":"https://docs.google.com/document/d/1aXJLZCs0t2jxeGO56RXKamUc4QJV35WER6IOt96ckao/edit?tab=t.0#heading=h.l1tzbowp9ywo",
     "drg":"https://etro.gg/gearset/72272317-821d-42ec-a1ea-70e7ecf4408f",
     "nin":"https://xivgear.app/?page=sl|5ff3583f-d784-4249-9e6d-2819e5e7b35f",
     "sam":"https://xivgear.app/?page=sl|df3e45d1-55d1-4bf9-a378-556f3685621e",
     "rpr":"https://xivgear.app/?page=sl|1cf30cb3-3fb2-47b9-a500-d8b117791a8e",
     "vpr":"https://xivgear.app/?page=sl|ce9f489d-413f-41c7-b6ee-72f9a20992fd",
     "brd":"https://xivgear.app/?page=sl%7C08860f73-14b1-4f10-889a-5ae60195f764",
     "mch":"https://xivgear.app/?page=sl|70a7b7f6-f09d-40f0-be34-ee7a27db22fa",
     "dnc":"https://xivgear.app/?page=sl|2af8238e-4b85-4308-b0ab-33df7bb255ea",
     "blm":"https://xivgear.app/?page=sl%7C8b29ebd6-d3c5-4aa2-abd0-302e05546c72",
     "rdm":"https://xivgear.app/?page=sl|08dd91db-2932-4c14-bcab-e50936b7d407&selectedIndex=3",
     "smn":"https://xivgear.app/?page=sl|02243465-733d-4ee5-b92e-6e924fb4591c&selectedIndex=1",
     "pct":"https://xivgear.app/?page=sl%7C15490375-060a-47a2-80a7-da90a5554ed8"
}

top_bis = {
     "pld":"https://xivgear.app/?page=bis|pld|ultimate|top",
     "war":" https://xivgear.app/#/bis/war/ultimate/top",
     "drk":"https://xivgear.app/#/bis/drk/ultimate/top",
     "gnb":"https://xivgear.app/#/bis/gnb/ultimates/top",
     "whm":"https://xivgear.app/?page=sl%7Ce5e7057a-5b0a-4f37-910e-624787a97fcc",
     "sch":"https://xivgear.app/?page=sl%7C8c6abd67-375c-468b-ad28-0bf64fd7a650",
     "ast":"https://xivgear.app/?page=sl|f4ac5879-3fac-4886-abf9-560f3b05b5e3",
     "sge":"https://xivgear.app/?page=sl|a02b7800-5ee9-4ad3-a3af-2ecafd66e0c2",
     "mnk":"https://docs.google.com/document/d/1aXJLZCs0t2jxeGO56RXKamUc4QJV35WER6IOt96ckao/edit?tab=t.0#heading=h.l5yah2butitz",
     "drg":"https://etro.gg/gearset/7593a2bb-23f0-4732-b650-e914f05de91c",
     "nin":"https://etro.gg/gearset/9f28fd54-55fe-4814-aee1-f19e419d95d0",
     "sam":"https://xivgear.app/?page=sl|3b86e3ce-871e-4f27-9354-ab98dba835dc",
     "rpr":"https://etro.gg/gearset/585d7c37-9d59-4a85-910e-e0a925b3cead",
     "vpr":"https://xivgear.app/?page=sl|56ae8077-eb7b-4b5d-a310-95cbd584f2a0",
     "brd":"https://media.discordapp.net/attachments/1047563703496740936/1423030325692465222/image.png?ex=68ded3c4&is=68dd8244&hm=be4135a21c2c1dfe87f74d8092d216ddee3abba3aa3eceba1578b081f2e7316e&=&format=webp&quality=lossless",
     "mch":"https://xivgear.app/?page=sl|09134793-0de2-45de-9743-270f076f3e16",
     "dnc":"https://xivgear.app/?page=sl|23d7dc27-198e-4de0-8493-5a59aa2d77ba",
     "blm":"https://xivgear.app/?page=sl|6480ebbb-a180-4401-a7c9-650d253c65b7",
     "rdm":"https://xivgear.app/?page=sl|405899e6-a9dd-44d5-a355-0004dd1b5142&selectedIndex=0",
     "smn":"https://xivgear.app/?page=sl|ea531021-b9c2-4ccc-8cd4-66c1f7d5117e&selectedIndex=5",
     "pct":"https://etro.gg/gearset/09995124-50cc-4888-8fa4-877a19cd1175"
}

dsr_bis = {
     "pld":"https://xivgear.app/?page=bis|pld|ultimate|dsr",
     "war":"https://xivgear.app/#/bis/war/ultimate/dsr",
     "drk":"https://xivgear.app/#/bis/drk/ultimate/dsr",
     "gnb":"https://xivgear.app/#/bis/gnb/ultimates/dsr",
     "whm":"https://xivgear.app/?page=sl%7C89cfa886-a885-4bc7-be5f-b86031cda39f",
     "ast":"https://etro.gg/gearset/94febc10-6779-486b-b57f-7993b766f41e",
     "sge":"https://xivgear.app/?page=sl|7833cd23-be46-455f-ad4d-be468928ea56",
     "mnk":"https://docs.google.com/document/d/1aXJLZCs0t2jxeGO56RXKamUc4QJV35WER6IOt96ckao/edit?tab=t.0#heading=h.kpqzig39dis7",
     "drg":"https://etro.gg/gearset/555df43d-4012-4757-96da-3f68fca985d0",
     "nin":"https://etro.gg/gearset/5914d3fa-14eb-494c-92be-5e05e12e08d9",
     "sam":"https://xivgear.app/?page=sl|e1869fb8-be98-41da-baf5-f27d2b94472a",
     "rpr":"https://etro.gg/gearset/2f655c79-6db1-4e5b-90f7-41e130bed30a",
     "vpr":"https://xivgear.app/?page=sl|48b50415-eb38-4d8f-80c8-ff7a5f15f987",
     "brd":"https://media.discordapp.net/attachments/1047563703496740936/1423030325692465222/image.png?ex=68ded3c4&is=68dd8244&hm=be4135a21c2c1dfe87f74d8092d216ddee3abba3aa3eceba1578b081f2e7316e&=&format=webp&quality=lossless",
     "mch":"https://xivgear.app/?page=sl|45acbe2d-f4f5-4a5e-9814-33af55134f29",
     "dnc":"https://xivgear.app/?page=sl|a6916eab-1fac-4921-adb8-420b5bc66677",
     "blm":"[High SPS](https://xivgear.app/?page=sl%7Cd1d8c2a1-da5b-4441-b047-5427ff4e8fe5) or [High CRT](https://xivgear.app/?page=sl%7C307bf5a3-d871-42f5-8095-ecd17b8ef823)",
     "rdm":"https://xivgear.app/?page=sl|405899e6-a9dd-44d5-a355-0004dd1b5142&selectedIndex=0",
     "smn":"https://etro.gg/gearset/7788d3ad-ed32-4f75-8aae-13f342f13f98",
     "pct":"https://etro.gg/gearset/99a6a79b-17d8-4f62-9c98-912b9fd238ca"
}

class cogName(commands.Cog):
    description="Uses BiS sets from TheBalance/IcyVeins to provide direct link to sets, quickly."
    def __init__(self,bot):
        self.bot = bot

    # Print code here
    @commands.command(name="bis", help="offers help with the BiS for a certain class for the current in-progress content", usage="[job] [fight](optional)")
    async def bis(self, ctx, job=None, fight=None):
         if job==None and fight==None:
            helpEmbed = discord.Embed(color=defaultEmbedColor, title=f"Check out your BiS for any job!", description="$bis [job] [fight](optional)")
            await ctx.reply(embed=helpEmbed)
         if job != None and job.lower() not in ["pld","war","drk","gnb","whm","sch","ast","sge","mnk","drg","nin","sam","rpr","vpr","brd","mch","dnc","blm","rdm","smn","pct"]:
            errorEmbed = discord.Embed(color=red, title=f"{xmark} Please provide a job to search BiS for!", description="Make sure you are using the 3 letter notation of your job! (ex: SGE)")
            await ctx.reply(embed=errorEmbed)
            return
         if fight != None and fight.lower() in ["tea", "ucob", "uwu"]:
            successEmbed = discord.Embed(color=green, title=f"{checkmark} According to IcyVeins, BiS sets for these fights are not included for all jobs, using current BiS is good enough!", description="You can find out your current BiS using $bis [job]")
            await ctx.reply(embed=successEmbed)
            return
         if fight != None:
            fight = fight.lower()
         if job != None:
            job = job.lower()

         bis_link = ""
         match fight:
              case "fru":
                 bis_link = fru_bis[job]
              case "top":
                 bis_link = top_bis[job]
              case "dsr":
                 bis_link = dsr_bis[job]
              case _:
                 bis_link = current_bis[job]
        
         bisEmbed = discord.Embed(color=green, title=f"{checkmark} BiS for {job.upper()}", description=f"{bis_link}")
         await ctx.reply(embed=bisEmbed)
         return
            
                   
         
         

        
async def setup(bot):
	await bot.add_cog(cogName(bot))
