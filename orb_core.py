"""
Main controller for Orb, also handles some basic commands & functions

Use the following link to add the bot:
https://discordapp.com/oauth2/authorize?client_id=569758271930368010&scope=bot&permissions=64
"""

# Imports libraries needed
import discord
import random
import os
import csv
import re
import sys
from google.cloud import firestore
from discord.ext import commands as bot_commands

# Gets constants from files. Yay interlinking
from cogs.orb_control import allowed_channel, db #TODO: Move Firestore into a util module (db.py?)
from utils import repo, logger
logger.log("core", "\n\n---BOOT COMPLETE---\nBase libraries successfully loaded")

# Assigns bot & client
bot = bot_commands.Bot(command_prefix=repo.get_prefix, help_command=None, case_insensitive=True)
client = discord.Client()

# Loads all the extensions 
files = os.listdir('cogs')
for cog in repo.config['disabled_cogs']:
    try:
        files.remove(f"{cog}.py")
    except:
        logger.log("core", f"Failed to remove {cog}. Is it present?")

for file in files:
    if file.endswith('.py'):
        file_name = file[:-3]
        bot.load_extension(f'cogs.{file_name}')
        logger.log("core", str(file_name) + '.py loaded!')
logger.log("core", 'Just a little bit more...')

bot.run(repo.get_token(), bot=True, reconnect=True)

# Orb bot help text (TODO: fix this so that it displays the built-in help command in Discord.py instead) 
@bot.command()
async def help(ctx):
    if allowed_channel(ctx):
        logger.log("core", f"Help request received from {ctx.author.display_name}")
        await ctx.send(u"Orb bot is a bot that does things. Features include:\n   - Reactions\n   - Posting Illya\n   - Ranking\nFor a list of commands see orb.commands, or check them out online at https://aribowe.github.io/orb/commands. To check the bot status, see orb.status.\nDeveloped by xiii™#0013 and 🌸Julianne🌸#6939.")

# Lists commands
@bot.command()
async def commands(ctx, target=None):
    if allowed_channel(ctx):
        await ctx.send("I have a lot of commands, visit https://aribowe.github.io/orb/commands to see them all")


