import discord

from discord.ext import commands as bot_commands

VERSION_DATA = {
            "Colour": "Sinopia",
            "Version": 7,
            "Build": 4,
            "ColourHex": 0xcb410b
        }

ONLINE_STATUS = "Online"

# Get prefixes
def get_prefix(bot, message):
    PREFIXES = ["orb.", "o."]
    return bot_commands.when_mentioned_or(*PREFIXES)(bot, message)