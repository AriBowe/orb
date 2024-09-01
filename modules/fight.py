import json, asyncio, discord
from datetime import datetime, timedelta
from discord.ext import commands

import utils.logger, utils.csv
from utils.util_csv import *

modDef = json.loads("""{
    "type": "fight",
    "name": "fight",
    "standalone": 0,
    "requires": [
    ],
    "provides": [
    ]
}""")

log = utils.logger.register(modDef['type'])

class FightModule(commands.Cog):
    def __init__(self, bot):
        self.players = utils.csv.connect("players")
        self.players.update()
        self.players.save()

async def setup(bot):
    await bot.add_cog(FightModule(bot))