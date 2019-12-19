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

# Get prefixes
def get_prefix(bot, message):
    return bot_commands.when_mentioned_or(*PREFIXES)(bot, message)
