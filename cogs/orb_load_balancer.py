"""
Load balancer is an optional cog which will automatically
apply various levels of slowmode upon message activity.
Draws data from orb_monitor.
"""

import discord
from datetime import datetime, timedelta
import asyncio
from discord.ext import commands as bot_commands
from utils import repo

class LoadCog(bot_commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.switch = True
        self.active_users = {}
        self.message_counter = 0
        self.message_log = [datetime(year=2000, month=1, day=1)] * 2
        self.fallback_counter = 0
        self.is_slowed = False

    @bot_commands.Cog.listener()
    async def on_message(self, ctx):
        # Control switch
        if not self.switch:
            return

        # Append most recent message to active users list
        user = ctx.author.id
        self.active_users[user] = datetime.now()        

        print("tick")

        # Message counter, will only read every 10 messages for performance
        self.message_counter += 1
        if self.message_counter >= 10:
            self.message_counter = 0

            guild_id = ctx.guild.id
            delete_list = []

            for user in self.active_users:
                if (datetime.now() - self.active_users[user]).total_seconds() > repo.LOAD_BALANCER[str(guild_id)]['active_timeout']:
                    self.active_users.pop(user)

        else:
            return
            
        # Gathering variables
        newest_message = ctx.created_at
        oldest_message = self.message_log.pop(0)
        self.message_log.append(newest_message)

        # Switch
        if (((newest_message - oldest_message).total_seconds() < 60)
                and len(self.active_users) >= repo.LOAD_BALANCER[str(guild_id)]['min_active']):
            poll = await ctx.channel.send("This channel seems quite active. Would you like me to enable a 5 second slow mode?")
            await poll.add_reaction("✅")
            await poll.add_reaction("❎")
        else:
            self.fallback_counter += 1
            if ((self.fallback_counter >= 3 
                    or (newest_message - self.message_log[-2]).total_seconds() > 60)
                    and self.is_slowed == True):
                await ctx.channel.send("Channel activity has dropped, lifting slowmode")
                ctx.channel.edit(slowmode_delay = 0, reason="Channel activity dropped")



        # Get user
        # Add user to active users list
        # message_counter++
        # if message_counter < 10, return. Else message_counter = 0
        # Get message time
        # Append time to message list
        # Pop time[0]
        # if delta(time[0], time) < stage_two_time:
        #   push slowmode message
        #   if pass
        #       set slowmode to 10s
        # else if delta(time[0], time) < stage_two_time:
        #   push slowmode message
        #   if pass
        #       set slowmode to 5s
        # else
        #   return

    @bot_commands.command(aliases=["balancer", "load_balancer"])
    async def toggle_balancer(self, ctx, switch="status"):
        if  (switch == "1" 
                or switch.upper() == "TRUE"
                or switch.upper() == "ON"):
            self.switch = True
            await ctx.send("Load balancer enabled")
        elif (switch == "0" 
                or switch.upper() == "FALSE" 
                or switch.upper() == "OFF"):
            self.switch = False
            await ctx.send("Load balancer disabled")
        else:
            await ctx.send(f"Load balancer online: {self.switch}\nUse `o.load_balancer on` to enable, or `o.load_balancer off` to disable")

# class User():
#     def __init__(self, user_id):
#         self.last_message = datetime.now()
#         self.id = user_id
        
#     def __eq__(self, comp):
#         return self.id == comp
    
#     def new_message(self):
#         self.last_message = datetime.now()

def setup(bot):
    bot.add_cog(LoadCog(bot))