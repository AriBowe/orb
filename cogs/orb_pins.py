"""
Pin cog

Pin code adapted from qbot, by Quantum Cucumber
Check the bot out at https://github.com/Quantum-Cucumber/quantum-bot
"""

import discord
from datetime import datetime, timedelta
import asyncio
import json
from discord.ext import commands as bot_commands
from utils import repo

class PinCog(bot_commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pins_store = []
        self.active_servers = []

        for server in repo.PIN_DATA:
            self.active_servers.append(int(server))

    @bot_commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        ctx = reaction.message

        is_pushpin = "📌" == str(reaction.emoji)
        guild_id = ctx.guild.id
        reaction_count = reaction.count
        
        async def pin_message(self, ctx, guild_id, pin_channel):
            message_id = ctx.id
            if str(message_id) in self.pins_store:
                return
                
            posted_message = discord.Embed(description=str(ctx.content), colour=0xcb410b)
            posted_message.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            if ctx.attachments != []:
                posted_message.set_image(url=ctx.attachments[0].url)
            posted_message.set_footer(text=(ctx.created_at + timedelta(hours=10)).strftime("%d %b %Y at %I:%M%p AEST"))
           
            await self.bot.get_channel(pin_channel).send("Message pinned from " + ctx.channel.mention + ". Context: https://www.discordapp.com/channels/" + str(guild_id) + "/" + str(ctx.channel.id) + "/" + str(message_id), embed=posted_message)
            self.pins_store.append(str(message_id))
            print("Pinned a message")

        if (is_pushpin 
                and guild_id in self.active_servers
                and (ctx.channel.id != repo.PIN_DATA[str(guild_id)]['pin_channel']
                and ctx.channel.id not in repo.PIN_DATA[str(guild_id)]['excluded_channels'])
                and reaction_count >= repo.PIN_DATA[str(guild_id)]['reaction_count']):
            await pin_message(self, ctx, guild_id, int(repo.PIN_DATA[str(guild_id)]['pin_channel']))
        
    @bot_commands.command()
    async def delete(self, context, channel, message_id):
        if context.author.id == 138198892968804352:
            ctx = await self.bot.get_channel(int(channel)).fetch_message(int(message_id))
            try:
                await ctx.delete()
                await context.send("Done")
            except:
                await context.send("Error")

    @bot_commands.command()
    async def pin(self, context, channel_id, pin_id):
        if context.author.id == 138198892968804352:
            ctx = await self.bot.get_channel(int(channel_id)).fetch_message(int(pin_id))

            posted_message = discord.Embed(description=str(ctx.content), colour=0xcb410b)
            posted_message.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            if ctx.attachments != []:
                posted_message.set_image(url=ctx.attachments[0].url)
            posted_message.set_footer(text=(ctx.created_at + timedelta(hours=10)).strftime("%d %b %Y at %I:%M%p AEST"))
            
            await self.bot.get_channel(606104185875857419).send("Message pinned from " + ctx.channel.mention, embed=posted_message)

    @bot_commands.command()
    async def exec(self, ctx, target):
        eval(str(target))

def setup(bot):
    bot.add_cog(PinCog(bot))
