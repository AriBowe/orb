import discord
from datetime import datetime, timedelta
import asyncio
from discord.ext import commands as bot_commands
from discord.ext import tasks

class FridayCog(bot_commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    @bot_commands.Cog.listener()
    async def on_ready(self):
        await self.announcement.start()

    @tasks.loop(minutes=1.0)
    async def announcement(self):
        channel = self.bot.get_channel(286411114969956352)
        current = datetime.now()
        if (current.strftime("%a") == "Thu" and current.strftime("%H") == "23" and current.strftime("%M") == "00"):
            await channel.send(file=discord.File(fp="images/happyFriday.mp4"))
            await channel.send("SMACK! Happy Friday!")
            
def setup(bot):
    bot.add_cog(FridayCog(bot))