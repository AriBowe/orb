import discord
from discord.ext import commands as bot_commands
import random
import csv
import re
import asyncio
from google.cloud import firestore

from cogs.orb_control import allowed_channel, db

class FightCog(bot_commands.Cog):
    """
    Main control class for managing Fights and Players.
    """
    def __init__(self, bot):
        self.bot = bot

        print("orb_fight loaded")

    @bot_commands.command()
    async def fight(self, ctx, target=None):
        """
        Begins a fight between two players

        Returns: None
        """
        if not allowed_channel(ctx):    # Verifies channel perms
            return None

        if target is None:              # Verifies that there is one target
            await ctx.send("You can't fight nothing")
            return None
        elif len(ctx.message.mentions) != 1:
            await ctx.send("Please tag a user to fight them")
            return None
        else:
            print(ctx.author.display_name + " is fighting " + target)

        target = ctx.message.mentions[0].id
        caller = ctx.author.id

        Fight(caller, target)


class Player():
    """
    A representation of a player of the game. A player can participate in Fights against another Player. A player can only participate in one fight at a time.
    """
    def __init__(self, player_id):
        self.hp = 5                         # Initial HP value
        self.hp_gain = 0                    # HP gained per turn
        self.mp = 5                         # Initial MP value
        self.mp_gain = 5                    # MP gained per turn
        self.mp_max = 30                    # Max MP possible
        
        self.effects = []                   # Current status effects
        self.cards = []                     # Cards in hand
        self._deck = self.populate_deck()   # Fills the player's deck

        self.id = player_id

        await self.load_player_info()

    async def load_player_info(self):
        """
        Loads player information from the Firestore server.

        Returns (dict): Player information
        """

        try:
            doc_ref = db.collection(u'fight').document(self.id)
            self._player_data = doc_ref.get().to_dict()
        except:
            await self._generate_player_info()

    async def _generate_player_info(self):
        """
        Generates initial player information and pushes to the Firestore server

        Returns (dict): Player information
        """
        data = {
            "victories": 0,
            "defeats": 0,
            "tables_flipped": 0,
            "longest_streak": 0
        }

        await db.collection('fight').document(self.id).set(data)

    async def record_victory(self):
        raise NotImplementedError

    async def record_defeat(self):
        raise NotImplementedError

    async def change_hp(self, value):
        raise NotImplementedError

    async def change_hp_gain(self, value):
        raise NotImplementedError

    async def change_mp(self, value):
        raise NotImplementedError

    async def change_mp_gain(self, value):
        raise NotImplementedError

    async def gain_card(self, card):
        raise NotImplementedError

    async def lose_card(self, card):
        raise NotImplementedError

    async def populate_deck(self):
        """
        Fills the player's deck with cards in a random order (shuffled)

        Returns (List): A filled, shuffled deck
        """
        raise NotImplementedError

    async def draw_card(self):
        raise NotImplementedError

class Fight():
    """
    A representation of a fight. A fight occurs between two Players, and always results in one victor and one loser. The Players play a card-based game in order to determine the winner and loser. Multiple fights can happen concurrently.
    """
    def __init__(self, player_1, player_2):
        self.player_1 = Player(player_1)
        self.player_2 = Player(player_2)

        self._run_game_loop()

    async def _run_game_loop(self):
        """
        The main game loop, in which Players take turns using Cards against their opponent.

        Returns: None
        """
        while True:
            if not await self._take_turn(self.player_1, self.player_2):
                break
            if not await self._take_turn(self.player_2, self.player_1):
                break

    async def _take_turn(self, active_player, enemy_player):
        """
        The active player taking their turn.

        Returns (bool): If the player has died or otherwise lost the game
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