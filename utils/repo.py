"""
Datastore for bot-wide constants, seperated so that it's easier to edit. Do NOT define these in other places please
"""

import discord

from discord.ext import commands as bot_commands

VERSION_DATA = {
            "Colour": "Sinopia",
            "Version": 8,
            "Build": 1,
            "ColourHex": 0xcb410b
        }

ONLINE_STATUS = "Online"

MESSAGE = "with orbs. Try orb.help"

PREFIXES = ["orb.", "o."]

ADMINS = [138198892968804352, 163067536693395456]

# Get prefixes
def get_prefix(bot, message):
    return bot_commands.when_mentioned_or(*PREFIXES)(bot, message)
