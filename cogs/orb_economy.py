import discord
from discord.ext import commands as bot_commands
import csv
import random

class User():
    """An orb user, this class manages their economy"""
    def __init__(self):
        pass

    async def get_orbs(self, user_id):
        with open("data/orbs.csv", mode="r", newline="") as file:
                reader = csv.reader(file, delimiter=",")
                for line in reader:
                    try:
                        print(line[0])
                        if line[0] == user_id:
                            return line[2]
                    except:
                        pass

    async def add_orbs(self, user_id, orb_type, orb_count):
        pass

    async def remove_orbs(self, user_id, orb_type, orb_count):
        pass

    async def get_shards(self, user_id):
        pass

    async def add_shards(self, user_id, shard_count):
        pass

    async def remove_shards(self, user_id, shard_count):
        pass

    async def save(self):
        pass

class Orb():
    """Representation of an orb, the basic unit of an item.
    Should not be initialised on its own"""
    def __init__(self):
        pass
    
    async def get_type(self):
        pass

    async def get_integrity(self):
        pass

    async def get_rarity(self):
        pass