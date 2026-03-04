# Atlas
This is a Discord bot I made for my own server as a way to accomplish 3 big goals.

Replace all of the 3rd party discord bots already in the server to make 1 "do-it-all" bot that I controlled.
Use my newly built headless Linux server to gain experience in unix-based coding, as well as learning VIM.
Rebuild my original bot, The Entity, from the ground up, with an easier to read codebase and added functionality to support plug-n-play cogs

After the huge success that was the birth of this bot, I set my sights higher, utilizing many other API's to create capabilities that other Discord bots can't offer. Since then it has been a constantly improving service I run, that runs alongside some of my other smaller projects, such as my hosted Minecraft servers.

Due to the nature of this bots birth, I apologize for the mess of the code. Initially its source code was never meant to see the light of day but the growing interest in it kinda made me realize that posting it here would help others like me develop something even better. This time around I've made many improvements to the comments, but at the moment a lot of the knowledge is subject to your own knowledge of Python.

Thank you to those in The Campfire and those who continue to show me and the bot support through our endless improvements!

What it does
I used a lot of API's over the development of this project to facilitate its functions. A comprehensive list can be found in the /cogs/ folder, where the functions are separated into their own (categorized) .py files. However some functions to note are:

Conversating with The Entity using its @ mention
Recording and wishing people a happy birthday on their birthdays
Good morning texts that send at a specific time every day
Personal DMs to people that want daily reminders
AI image generation based on a given prompt
Changing the banner and icon of discord server to match the themes of the year
API's Used
Below are some of the API's that I have used in the development of this bot, to help users have more fun with its functionality

discord.py API library for making all of this possible
OpenAI's gpt-4 (and its predecessor, gpt-3.5-turbo)
OpenAI's Dall-E engine for image generation
Riot's API (featured in the now-retired league of legends lookup)
davidteather's Unofficial TikTok API (featured in the now-retired TikTok embedder)
Tenor's API for gif searching
Musixmatch's API for the under development $lyrics function
Not Included
As expected, some code is left out for security reasons because they manage my Minecraft servers, which contains IP's and the like. However because I know the scripts are referenced in some of the code I'll go over what they do in case anyone is wondering:

reboot.sh: reboots the minecraft servers (uses codenames like TNT or MMC to denote which server needs restarting, but other than that, doesn't do much else)
update.sh: pushes changes locally to my live version of The Entity. The bot runs in a separate destination due so that I can make changes locally without having to turn the bot off and on to make these changes. In the future I aim to have a second, local bot that I use to test these changes live before I push them. That is for another day, however.
rollback.sh: this is the "undo" button of sorts. It has since been deprecated, as it was only used back when the bot ran as 1 single file (before I made the switch to using Cogs).
At the moment, this bot is not available for other servers. While some functions will work across multiple servers, a lot of functions were designed for one server only, and as such, this version of the bot will not be available to the public. If you choose to reuse any of the code I have written, please just make sure to give credit! :)
