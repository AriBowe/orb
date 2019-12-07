import discord
from discord.ext import commands as bot_commands
import random
import csv
import re
import asyncio
from google.cloud import firestore

from cogs.orb_control import allowed_channel

class FightCog(bot_commands.Cog):
    """
    Main control class for managing Fights and Players.
    """
    def __init__(self, bot):
        self.bot = bot
        self._current_fights = []

        print("orb_fight loaded")

    @bot_commands.command()
    async def fight(self, ctx, target=None):
        """
        Begins a fight between two players

        Returns: None
        """
        raise NotImplementedError

class Player():
    """
    A representation of a player of the game. A player can participate in Fights against another Player. A player can only participate in one fight at a time.
    """
    def __init__(self):
        self.hp = 5             # Initial HP value
        self.hp_gain = 0        # HP gained per turn
        self.hp_max = 10        # Max HP possible
        self.mp = 5             # Initial MP value
        self.mp_gain = 5        # MP gained per turn
        self.mp_max = 30        # Max MP possible
        
        self.effects = []       # Current status effects

    async def load_player_info(self):
        """
        Loads player information from the Firestore server.

        Returns (dict): Player information
        """
        raise NotImplementedError

    async def _generate_player_info(self):
        """
        Generates initial player information and pushes to the Firestore server

        Returns (dict): Player information
        """
        raise NotImplementedError

    async def record_victory(self):
        raise NotImplementedError

    async def record_defeat(self):
        raise NotImplementedError

class Fight():
    """
    A representation of a fight. A fight occurs between two Players, and always results in one victor and one loser. The Players play a card-based game in order to determine the winner and loser. Multiple fights can happen concurrently.
    """
    def __init__(self):
        raise NotImplementedError

    async def _game_loop(self, active_player):
        """
        The main game loop, in which a Player selects and uses Cards against their opponent.

        Returns: None
        """
        raise NotImplementedError

    async def _play_card(self, active_player):
        """
        The action of playing/using a card.

        Returns: None
        """
        raise NotImplementedError

    async def _game_end(self, victor, loser):
        raise NotImplementedError

    async def _change_hp(self, target):
        raise NotImplementedError

    async def _change_mp(self, target):
        raise NotImplementedError

class Card():
    def __init__(self, owner):
        raise NotImplementedError

    async def play(self, owner):
        raise NotImplementedError

def setup(bot):
    bot.add_cog(FightCog(bot))