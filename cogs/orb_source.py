"""
Detects the source of an image using the unofficial saucenao API
"""

import discord
from discord.ext import commands as bot_commands
from saucenao_api import SauceNao
from utils import repo, logger
class SauceCog(bot_commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bot_commands.command(aliases=["source"])
    async def sauce(self, ctx):
        if ctx.message.reference == None:
            await ctx.send("This command only functions when used in a reply!")
            return
        
        source = SauceNao(api_key=repo.config["keys"]["saucenao_api_key"])

        reference = await ctx.channel.fetch_message(ctx.message.reference.message_id)
        if len(reference.attachments) > 0 or len(reference.embeds):
            output = ""
            for attachment in reference.attachments:
                try:
                    output += f"\n{source.from_url(attachment.url)[0].urls[0]} (similarity: {source.from_url(attachment.url)[0].similarity})"
                except Exception as e:
                    logger.log("Source", f"Failed to read attachment {attachment.url}. {e}")
            for embed in reference.embeds:
                try:
                    output += f"\n{source.from_url(embed.thumbnail.url)[0].urls[0]} (similarity: {source.from_url(embed.thumbnail.url)[0].similarity})"
                except Exception as e:
                    logger.log("Source", f"Failed to read embed {embed.thumbnail.url}. {e}")
            if len(output) > 0:
                await ctx.send(f"Here's my best guess at the sources: {output}")
            else:
                await ctx.send(f"Failed to read the message, you may have to manually reverse-search this one")
        else:
            await ctx.send("The replied message does not have any attachments, or could not be loaded.")

            


def setup(bot):
    bot.add_cog(SauceCog(bot))