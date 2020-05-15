"""
Datastore for bot-wide constants, seperated so that it's easier to edit. Do NOT define these in other places please
"""

import discord
import json

from discord.ext import commands as bot_commands

with open("..data/config.json", "r") as config:
    config = json.load(config)

# VERSION_DATA = {
#             "Colour": "Sinopia",
#             "Version": 9.2,
#             "Build": 1,
#             "ColourHex": 0xcb410b
#         }

VERSION_DATA = config[version_data]

ONLINE_STATUS = "Online"

MESSAGE = exec(config[message])

PREFIXES = ["orb.", "o."]

ADMINS = [138198892968804352, 163067536693395456]

# Get prefixes
def get_prefix(bot, message):
    return bot_commands.when_mentioned_or(*PREFIXES)(bot, message)
