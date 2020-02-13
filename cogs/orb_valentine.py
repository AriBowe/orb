"""
Love is in the air! Assigns user random valentines. REMEMBER TO REMOVE THIS AFTER 2 WEEKS!!!
"""

# Standard module imports
import discord
import random

# Conditional module imports
from datetime import datetime, timedelta
from google.cloud import firestore
from discord.ext import commands as bot_commands

# Local bot imports
from utils import default, repo
from cogs.orb_control import allowed_channel, db




class Valentine(bot_commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._active_users = []
        self._last_active_check = datetime(2001, 9, 13)
        
        self.SMACK_GUILD = bot.get_guild(286411114969956352)
        self.SMACK_ID = 286411114969956352

    @bot_commands.command(aliases=["loves", "love", "valentine", "crush"])
    async def valentines(self, ctx, *, target=None):
        if ctx.guild.id != self.SMACK_ID:
            await ctx.send("Sorry, but my cherub powers only extend to SMACK UQ!")
            return

        if target == None:
            target = ctx.author.id
        elif len(ctx.message.mentions) == 1:
            target = ctx.message.mentions[0].id
        else:
            await ctx.send("Woah there! Please tag the person whose love you're questioning after the command, or don't put anything after the command to see your own love.")
            return

        crush = self.bot.get_user(await self._get_crush(ctx, target)).mention
        crushee = self.bot.get_user(target).display_name

        await ctx.send(random.choice([f"{crushee}, your valentine's crush is {crush}!", f"{crushee}, you're hopelessly in love with {crush}", f"Your eye has recently been caught by {crush}, hasn't it {crushee}?"]))
        return

    async def _get_crush(self, ctx, user_id):
        """
        Checks Firestore to see if this user already has a crush, and if not, generates one
        """

        doc_ref = db.collection('valentines').document(str(user_id))
        results = doc_ref.get().to_dict()

        if not results:
            return await self._generate_crush(ctx, user_id)

        return results["crush"]

    async def _generate_crush(self, ctx, user_id):
        """
        Receives a random active user and stores them as a user's crush
        """
        crush_id = await self._find_random_active_user(ctx)
        data = {
            "crush": crush_id
        }

        db.collection('valentines').document(str(user_id)).set(data)

        return crush_id

    async def _find_random_active_user(self, ctx):
        """
        Picks and returns a user at random from a list of users who have been active in the past week. Uses basic caching to speed up performance
        """

        if self._last_active_check < datetime.utcnow() + timedelta(minutes=5):
            active_users = self.SMACK_GUILD.get_role(371079720768634895)        # Execs
            active_users.append(self.SMACK_GUILD.get_role(592939685723242496))  # Mods
            active_users.append(self.SMACK_GUILD.get_role(286412638508941312))  # Senpai
            active_users.append(self.SMACK_GUILD.get_role(286411614855626752))  # Old Exec
            active_users.append(self.SMACK_GUILD.get_role(585601647149842465))  # Boost
            active_users.append(self.SMACK_GUILD.get_role(607914165121843230))  # Member

            self._last_active_check = datetime.utcnow()
            self._active_users = active_users            
        
        return random.choice(self._active_users).id


def setup(bot):
    bot.add_cog(Valentine(bot))