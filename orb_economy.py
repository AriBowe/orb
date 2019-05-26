import discord
from discord.ext import commands as bot_commands
import csv
import random

class User(bot_commands.Cog):
    """An orb user, this class manages their economy"""
    def __init__(self):
        pass

    async def get_orbs(self):
        pass

    async def add_orbs(self, orb_type, orb_count):
        pass

    async def remove_orbs(self, orb_type, orb_count):
        pass


class Orb(bot_commands.Cog):
    """Representation of an orb, the basic unit of an item.
    Should not be initialsed on it's own"""
    def __init__(self):
        pass
    
    async def get_type(self):
        pass

    async def get_integrity(self):
        pass

    async def get_rarity(self):
        pass