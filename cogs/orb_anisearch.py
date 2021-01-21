"""
Interfaces with trace.moe to grab anime, episode, and timestamp info for a provided screenshot
"""

# Standard module imports
import discord
import random
import requests
import json

# Conditional module imports
from datetime import datetime, timedelta
from google.cloud import firestore
from discord.ext import commands as bot_commands

# Local bot imports
from utils import repo
from cogs.orb_control import allowed_channel, db




class AniSearch(bot_commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._active_users = []
        self._last_active_check = datetime(2001, 9, 13)

    @bot_commands.command(aliases=["search", "find", "trace"])
    async def aniSearch(self, ctx, **kwargs):
        self.SMACK_GUILD = self.bot.get_guild(286411114969956352)
        self.SMACK_ID = 286411114969956352

        # if ctx.guild.id != self.SMACK_ID:
        #     await ctx.send("Sorry, but my powers only extend to SMACK UQ!")
        #     return

        print(ctx.message.attachments)

        if(len(ctx.message.attachments) != 1):
            await ctx.send("I need an image to track down!")
            return

        request = requests.get(f'https://trace.moe/api/search?url={ctx.message.attachments[0].url}')
        response_json = request.json()
        print(response_json["docs"][0])
        top_result = response_json['docs'][0]

        title = top_result['title_english']
        desc = f'Episode {top_result["episode"]} at {str(timedelta(seconds=top_result["at"]))}'
        url = f'https://anilist.co/anime/{top_result["anilist_id"]}'

        embed = discord.Embed(title=title, description=desc, url=url)
        embed.set_footer(text=f"Confidence: {top_result['similarity'] * 100}%")
        embed.set_image(url=ctx.message.attachments[0].url)
        await ctx.send(f"Here's what I found:", embed=embed)

        return

def setup(bot):
    bot.add_cog(AniSearch(bot))
