"""
Synergy is a cog designed to bring direct democratic systems to Discord moderation.
This is an optional bot feature that should be configured using the config.json file.

🦀
"""

import discord
from datetime import datetime, timedelta
import asyncio
import json
from discord.ext import commands as bot_commands

class SynergyCog(bot_commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pins_store = []
                

    """
    Command parser (needed because all synergy commands are formatted as sub-commands)
    """
    @bot_commands.command(aliases=["syn"])
    async def synergy(self, ctx):
        command, arguments = ctx.content.split(" ", 1)
        arguments = arguments.split(" ")

        if command == "channel":
            pass
        else:
            ctx.send("Synergy internal error: Command not recognised")

class Synergy():
    def __init__(self, bot):
        pass


def setup(bot):
    bot.add_cog(SynergyCog(bot))
