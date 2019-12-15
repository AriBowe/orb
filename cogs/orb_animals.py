import random

from discord.ext import commands

from utils.reddit_scraper import reddit_imgscrape


class Animals(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['kitten'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def kittens(self, ctx):
        """/r/kittens"""
        kitten_url = 'https://www.reddit.com/r/kittens/.json'
        await reddit_imgscrape(ctx, kitten_url)

    @commands.command(alises=['cat'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def cats(self, ctx):
        """Cat pictures retrieved from lots of different subreddits!"""
        cats_url = [
            'https://www.reddit.com/r/cats/',
            'https://www.reddit.com/r/LazyCats/',
            'https://www.reddit.com/r/StuffOnCats/',
            'https://www.reddit.com/r/SupermodelCats/',
            'https://www.reddit.com/r/TheCatTrapIsWorking/',
            'https://www.reddit.com/r/TuxedoCats/',
            'https://www.reddit.com/r/blackcats/'
        ]

        random.shuffle(cats_url)
        await reddit_imgscrape(ctx, random.choice(cats_url) + '.json')

    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def catbellies(self, ctx):
        """/r/catbellies"""
        await reddit_imgscrape(ctx,  'https://www.reddit.com/r/catbellies/.json')

    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def catsonkeyboards(self, ctx):
        """/r/CatsOnKeyboards"""
        await reddit_imgscrape(ctx, 'https://www.reddit.com/r/CatsOnKeyboards/.json')

    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def kneadycats(self, ctx):
        """/r/KneadyCats"""
        await reddit_imgscrape(ctx, 'https://www.reddit.com/r/KneadyCats/.json')

    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def catloaf(self, ctx):
        """/r/Catloaf"""
        await reddit_imgscrape(ctx, 'https://www.reddit.com/r/Catloaf/.json')


    @commands.command(aliases=['catgif'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def catgifs(self, ctx):
        """/r/CatGifs"""
        gif_url = ['https://www.reddit.com/r/CatGifs/.json']

        await reddit_imgscrape(ctx, gif_url)

    @commands.command(aliases=['fox', 'foxer', 'foxers'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def foxes(self, ctx):
        """/r/foxes"""
        foxes_url = 'https://www.reddit.com/r/foxes/hot/.json'
        await reddit_imgscrape(ctx, foxes_url)

    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def foxgifs(self, ctx):
        """/r/foxgifs"""
        await reddit_imgscrape(ctx, 'https://www.reddit.com/r/foxgifs/hot/.json')

    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def foxloaf(self, ctx):
        """/r/foxloaf"""
        await reddit_imgscrape(ctx, 'https://www.reddit.com/r/foxloaf/.json')

    @commands.command(aliases=['shibe', 'shibas', 'shibes'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def shiba(self, ctx):
        """/r/shiba"""
        shibe_url = 'https://www.reddit.com/r/shiba/.json'

        await reddit_imgscrape(ctx, random.choice(shibe_url))

    @commands.command(aliases=['bird', 'birbs', 'birds'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def birb(self, ctx):
        """/r/birb"""
        birb_url = 'https://www.reddit.com/r/Birbs/.json'
        await reddit_imgscrape(ctx, birb_url)

    @commands.command(aliases=['eyebleach, cuteanimals'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def aww(self, ctx):
        """/r/aww"""
        cute_url = [
            'https://www.reddit.com/r/aww/.json'
        ]
        random.shuffle(cute_url)
        await reddit_imgscrape(ctx, random.choice(cute_url))

    @commands.command()
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def animalsbeingjerks(self, ctx):
        """/r/AnimalsBeingJerks"""
        jerk_url = 'https://www.reddit.com/r/AnimalsBeingJerks/.json'
        await reddit_imgscrape(ctx, jerk_url)

    @commands.command()
    @commands.cooldown(rate=1, per=5, type = commands.BucketType.user)
    async def eyebleach(self, ctx):
        """/r/EyeBleach"""
        eyebleach_url = 'https://www.reddit.com/r/Eyebleach/.json'
        await reddit_imgscrape(ctx, eyebleach_url)

    @commands.command(aliases=['aww_gifs', 'awwgif'])
    @commands.cooldown(rate=1, per=5, type=commands.BucketType.user)
    async def awwgifs(self, ctx):
        """Cute animal gifs!"""
        gif_url = 'https://www.reddit.com/r/aww_gifs/.json'
        await reddit_imgscrape(ctx, gif_url)


def setup(bot):
    bot.add_cog(Animals(bot))