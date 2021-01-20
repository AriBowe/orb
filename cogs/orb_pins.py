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

    # Detects pin reactions
    @bot_commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        ctx = reaction.message

        is_pushpin = "📌" == str(reaction.emoji)
        guild_id = ctx.guild.id
        reaction_count = reaction.count
        
        if (is_pushpin 
                and guild_id in self.active_servers
                and (ctx.channel.id not in repo.PIN_DATA[str(guild_id)]['pin_channels']
                and ctx.channel.id not in repo.PIN_DATA[str(guild_id)]['excluded_channels'])):
            
            # Target channel selector
            if str(ctx.channel.id) in repo.PIN_DATA[str(guild_id)]['channel_switches']:
                target_channel = repo.PIN_DATA[str(guild_id)]['channel_switches'][str(ctx.channel.id)]
            else:
                target_channel = 0

            # Pin it
            if reaction_count >= repo.PIN_DATA[str(guild_id)]['reaction_counts'][target_channel]:
                await self._pin_message(ctx, guild_id, int(repo.PIN_DATA[str(guild_id)]['pin_channels'][target_channel]))

    # Actual main pin function
    async def _pin_message(self, ctx, guild_id, pin_channel):
        message_id = ctx.id
        vid_mode = False

        # Checks if the message has already been pinned. Due to how Discord deals with messages,
        # we can ignore messages older than the current bot instance
        if str(message_id) in self.pins_store:
            return
            
        # Generate base embed    
        posted_message = discord.Embed(description=str(ctx.content), colour=0xcb410b)
        posted_message.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        
        # Manage attachments
        if ctx.attachments != []:
            vid_mode = ctx.attachments[0].url.split(".")[-1] in repo.config["video_formats"]

            if (not vid_mode):
                posted_message.set_image(url=ctx.attachments[0].url)
            else:
                posted_message.description += f" [{(ctx.attachments[0].url).split('/')[-1]}]"
        posted_message.set_footer(text=(ctx.created_at + timedelta(hours=10)).strftime("%d %b %Y at %I:%M%p AEST"))
        
        await self.bot.get_channel(pin_channel).send(f"Message pinned from {ctx.channel.mention}. context: https://www.discordapp.com/channels/{str(guild_id)}/{str(ctx.channel.id)}/{str(message_id)}", embed=posted_message)
        if(vid_mode):
            await self.bot.get_channel(pin_channel).send(ctx.attachments[0].url)                

        self.pins_store.append(str(message_id))
        logger.log_and_print("pins", f"Pinned message: '{str(ctx.content)}' by {ctx.author.display_name}. Attachments: {ctx.attachments == []}")

    @bot_commands.command()
    async def delete(self, ctx, channel, message_id):
        if ctx.author.id in repo.CONTROLLERS:
            ctx = await self.bot.get_channel(int(channel)).fetch_message(int(message_id))
            try:
                await ctx.delete()
                await ctx.send("Done")
            except:
                await ctx.send("Error")

    @bot_commands.command()
    async def pin(self, ctx, guild_id, channel_id, pin_id):
        if str(ctx.author.id) in repo.CONTROLLERS:
            ctx = await self.bot.get_channel(int(channel_id)).fetch_message(int(pin_id))

            # Target channel selector
            if channel_id in repo.PIN_DATA[guild_id]['channel_switches']:
                target_channel = repo.PIN_DATA[guild_id]['channel_switches'][channel_id]
            else:
                target_channel = 0

            await self._pin_message(ctx, guild_id, int(repo.PIN_DATA[guild_id]['pin_channels'][target_channel]))

def setup(bot):
    bot.add_cog(PinCog(bot))
