"""God is dead"""

# Standard imports
import discord
import random
from discord.ext import commands as bot_commands

# Local bot imports
from utils import repo
from cogs.orb_control import allowed_channel, db

class Gacha(bot_commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot_commands.command()
    async def gacha(self, ctx):
        await ctx.send(random.choice(["Double!","Nothing!"]))

def setup(bot):
    bot.add_cog(Gacha(bot))