import json, re, logging
import discord
from discord.ext import commands

modDef = json.loads("""{
    "type": "ball",
    "name": "Balls",
    "standalone": 1,
    "requires": [
    ],
    "provides": [
    ]
}""")

class BallsModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(self.__class__.__name__)
        self.target = None

    # Detects balls
    @commands.Cog.listener()
    async def on_message(self, ctx): 
        if (re.match(pattern="(ball)", string=ctx.content)):
            if self.target == None:
                self.target = await self.bot.fetch_user(364038762897866753)
                print(self.target)

            await self.target.send(f"Balls detected at {ctx.jump_url}")
            self.logger.info(f"Balls detected")

async def setup(bot):
    await bot.add_cog(BallsModule(bot))