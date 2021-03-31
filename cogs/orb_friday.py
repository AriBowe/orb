import discord
from datetime import datetime, timedelta
#import schedule
import asyncio
from discord.ext import commands as bot_commands
from discord.ext import tasks

#bot = bot_commands.Bot(command_prefix="o")
client = discord.Client()

class FridayCog(bot_commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @bot_commands.Cog.listener()
    async def on_ready(self):
        await self.announcement.start()

    @tasks.loop(minutes=1.0)
    async def announcement(self):
        channel = self.bot.get_channel(823075283942375458)

        current = datetime.datetime.now()
        if (current.strftime("%a") == "Fri" and current.strftime("%H") == "09" and current.strftime("%M") == "00"):
            channel.send("asd")
            
def setup(bot):
    bot.add_cog(FridayCog(bot))