"""
Echo is a cog which will record messages sent and repost them in the event
that they get edited or deleted. Only use this with permission and understanding
from the members of your server
"""

import discord
from datetime import datetime, timedelta
import asyncio
from discord.ext import commands as bot_commands

class EchoCog(bot_commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        

def setup(bot):
    bot.add_cog(EchoCog(bot))