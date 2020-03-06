import random


from utils.reddit_scraper import reddit_imgscrape
from discord.ext import commands

class Memes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def dankmemes(self, ctx):
        """/r/dankmemes"""
        dank_url = "https://www.reddit.com/r/dankmemes/.json"
        await reddit_imgscrape(ctx, dank_url)

    @commands.command(aliases=["meme"])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def memes(self, ctx):
        """/r/animemes"""
        meme_url = [
            "https://www.reddit.com/r/anime_irl/",
            "https://www.reddit.com/r/Animemes/"
        ]
        random.shuffle(meme_url)
        await reddit_imgscrape(ctx, random.choice(meme_url) + '.json')

def setup(bot):
    bot.add_cog(Memes(bot))
