import discord
import json, os, re, importlib, asyncio, unittest
from discord.ext import commands

# Load utils
from utils import *
from modules import *

# Intialise self-logging
log = logger.register("core")

# Request message reading intent
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="ob.", help_command=None, case_insensitive=True, intents=intents)
log("Client connection initiated")

# Load modules
async def load_mods():
    mods = [f[:-3] for f in os.listdir('modules') if re.match(r'.*[^__]\.py', f)]
    log(f"Begining module load. {len(mods)} item(s) detected\n\t\t\t\t------------")
    for mod in mods:
        await bot.load_extension(f"modules.{mod}")
        log(f"Module {mod} successfully loaded")

asyncio.run(load_mods())

@bot.event
async def on_ready():
    log("Bot successfully initialised", 2)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

with open("config/keys.json") as config:
    config = json.load(config)
    bot.run(config['keys']['test_token'], reconnect=True)