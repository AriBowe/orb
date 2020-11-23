"""
Datastore for bot-wide constants, seperated so that it's easier to edit. Do NOT define these in other places please
"""

import discord
import json

from discord.ext import commands as bot_commands

with open("data/config.json", "r") as config:
    config = json.load(config)

# VERSION_DATA = {
#             "Colour": "Sinopia",
#             "Version": 9.2,
#             "Build": 1,
#             "ColourHex": 0xcb410b
#         }

VERSION_DATA = config['version_data']
ONLINE_STATUS = config['message']
MESSAGE = eval(config['message'])
PREFIXES = config['prefixes']
CONTROLLERS = config['controllers']
BANNED_CHANNELS = "x"
PIN_DATA = config['optional_cogs']['pin_settings']
LOAD_BALANCER = config['optional_cogs']['load_balancer_settings']

# Get prefixes
def get_prefix(bot, message):
    return bot_commands.when_mentioned_or(*config['prefixes'])(bot, message)

# Get token
def get_token():
    if config['is_test']:
        return config['keys']['test_token']
    return config['keys']['token']