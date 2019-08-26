"""
Pin code adapted from qbot, by Quantum Cucumber
Check the bot out at https://github.com/Quantum-Cucumber/quantum-bot
"""

import discord
import datetime
import asyncio
import csv
from discord.ext import commands as bot_commands

class PinCog(bot_commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("orb_pins loaded")

    @bot_commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        ctx = reaction.message

        is_pushpin = "📌" == str(reaction.emoji)
        guild_id = ctx.guild.id
        reaction_count = reaction.count
        
        if is_pushpin and (guild_id == 286411114969956352) and ctx.channel.id != 606104185875857419 and reaction_count >= 5:
            with open("data/pin.csv", mode="r", newline="") as file:
                reader = csv.reader(file, delimiter=",")
                message_id = ctx.id
                for line in reader:
                    try:       
                        if str(message_id) in line:
                            return
                    except:
                        pass
                
            posted_message = discord.Embed(description=str(ctx.content), colour=0xcb410b)
            posted_message.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
            if ctx.attachments != []:
                posted_message.set_image(url=ctx.attachments[0].url)
            posted_message.set_footer(text=ctx.created_at.strftime("%d %b %Y at %H:%M%p"))
           
            await self.bot.get_channel(606104185875857419).send("Message pinned from " + ctx.channel.mention, embed=posted_message)
            with open("data/pin.csv", mode="a", newline="") as file:
                writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)    
                writer.writerow([message_id])
            print("Pinned a message")

    # @bot_commands.command()
    # async def backpin(self, context):
    #     with open("pin_ids.csv", mode="r", newline="") as file:
    #         reader = csv.reader(file, delimiter=",")
    #         for line in reader:
    #                 ctx = await self.bot.get_channel(371256177872338945).fetch_message(int(line[0]))

    #                 posted_message = discord.Embed(description=str(ctx.content), colour=0xcb410b)
    #                 posted_message.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
    #                 if ctx.attachments != []:
    #                     posted_message.set_image(url=ctx.attachments[0].url)
    #                 posted_message.set_footer(text=ctx.created_at.strftime("%d %b %Y at %H:%M%p"))
                    
    #                 await self.bot.get_channel(606104185875857419).send("Message pinned from " + ctx.channel.mention, embed=posted_message)
    #                 await asyncio.sleep(2)

    #         print("Done!")
        
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
    async def pin(self, context, channel_id, pin_id, server_id=606104185875857419):
        ctx = await self.bot.get_channel(int(channel_id)).fetch_message(int(pin_id))

        posted_message = discord.Embed(description=str(ctx.content), colour=0xcb410b)
        posted_message.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)
        if ctx.attachments != []:
            posted_message.set_image(url=ctx.attachments[0].url)
        posted_message.set_footer(text=ctx.created_at.strftime("%d %b %Y at %H:%M%p"))
        
        await self.bot.get_channel(606104185875857419).send("Message pinned from " + ctx.channel.mention, embed=posted_message)
        await asyncio.sleep(2)


def setup(bot):
    bot.add_cog(PinCog(bot))