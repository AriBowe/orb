import discord
import random
import sys
import datetime
import csv
import re
import traceback

from discord.ext import commands as bot_commands
from discord.ext.commands import errors
from http.client import HTTPException, HTTPResponse
from utils import repo, logger
from utils.repo import VERSION_DATA, MESSAGE, PREFIXES, REACTIONS
from cogs.orb_control import db


async def send_command_help(ctx):
    """
    Sends help message for specific command

    Params:
        (discord.ext.commands.Context) ctx: context
    """
    await ctx.send("That's not how you use this command! Try again, and check https://aribowe.github.io/orb/commands.html if you're not sure")

class Events(bot_commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    # Displays boot complete message
    
    @bot_commands.Cog.listener()
    async def on_ready(self):
        if not hasattr(self.bot, 'uptime'):
            self.bot.uptime = datetime.datetime.now()

        await self.bot.change_presence(status=discord.Status.online, activity=MESSAGE)
        logger.log_and_print("events", f"ORB Core {VERSION_DATA['Colour']} {VERSION_DATA['Version']} Build {VERSION_DATA['Build']}")
        logger.log_and_print("events", '------------------------------------------')
        logger.log_and_print("events", 'Bot is online and connected to Discord.')
        if len(self.bot.guilds) == 1:
            logger.log_and_print("events", f'Currently connected to {len(self.bot.guilds)} server.')
        else:
            logger.log_and_print("events", f'Currently connected to {len(self.bot.guilds)} servers.')
        logger.log_and_print("events", '------------------------------------------')
        logger.log_and_print("events", f'Bot Name: {self.bot.user.name}')
        logger.log_and_print("events", f'Bot ID: {str(self.bot.user.id)}')
        logger.log_and_print("events", '')
        logger.log_and_print("events", f'Discord.py Version: {discord.__version__}')
        logger.log_and_print("events", f'Python Version:  {sys.version[:5]}')
        logger.log_and_print("events", '')
        logger.log_and_print("events", f'orb.py Version: {str(repo.VERSION_DATA["Version"])}')
        logger.log_and_print("events", '------------------------------------------')
        

    @bot_commands.Cog.listener()
    async def on_command_error(self, ctx, error: errors):
        """
        Bot posts message when command errors occur

        Params:
            (discord.ext.commands.Context) ctx: Context
            (discord.ext.commands.errors): errors
        """
        logger.log("on_command_error", f"{ctx.message.author}: '{ctx.message.content}' ({ctx.message.id})")
        if isinstance(error, errors.CommandNotFound):
            await ctx.send(f'Invalid command. To see a list of commands visit https://aribowe.github.io/orb/.')

        elif isinstance(error, errors.MissingRequiredArgument) or isinstance(error, errors.BadArgument):
            await send_command_help(ctx)

        elif isinstance(error, errors.CommandOnCooldown):
            await ctx.send(f'Woah, slow down there! Retry again in {error.retry_after:.0f} seconds.')

        elif isinstance(error, errors.CommandInvokeError):

            _traceback = traceback.format_list(traceback.extract_tb(error.__traceback__))
            _traceback = ''.join(_traceback)

            error_message = f'```Python\n{_traceback}{type(error).__name__}: {error}```'

            await ctx.send(f'There was an error processing the command ;w; {error_message}')

        elif isinstance(error, errors.MissingPermissions):
            await ctx.send('You do not have the required permissions to run this command.')

        elif isinstance(error, errors.BotMissingPermissions):
            await ctx.send('I do not have permission to run this command ;w;')

        elif isinstance(error, HTTPException):
            # if HTTPResponse == 413:
            ctx.send('The file size is too large for me to send over Discord ;o;')

    # Disabled
    # @bot_commands.Cog.listener()
    # async def on_command(self, ctx):
    #     """Prints user commands to console"""
    #     try:
    #         logger.log("command", f'{ctx.guild.me} > {ctx.message.channel} > {ctx.message.author.name} > {ctx.message.clean_content}')
    #     except AttributeError:
    #         logger.log("command", f'Private Message > {ctx.message.channel} > {ctx.message.author.name} > {ctx.message.clean_content}')

    @bot_commands.Cog.listener()
    async def on_message(self, message):

        # Performs reactions as defined in the config
        for reaction in repo.REACTIONS:
            for trigger in reaction["triggers"]:
                if (re.search(fr"\b({trigger})\b", message.content, re.IGNORECASE) and random.random() < reaction["chance"]):
                    __resolved_weight = random.random()
                    for response in reaction["responses"]:
                        if response["weight_cutoff"] >= __resolved_weight:
                            if response["is_stream"]:
                                for emote in response["content"]:
                                    await message.add_reaction(emote)
                            else:
                                await message.add_reaction(self.bot.get_emoji(response["content"]))
                            logger.log("reaction", f"Responded with '{response['content']}' to message '{message.content}' from user {message.author.display_name}")
                            return

        # Big guy react
        if re.search(r"\b(big guy)\b", message.content, re.IGNORECASE) and random.random() > 0.75:
            await message.channel.send("For you")
            logger.log("reaction", f"Responded with 'For you' to message '{message.content}' from user {message.author.display_name}")

        # 3/10
        elif re.search(r"\b(asuna)\b", message.content, re.IGNORECASE) or re.search(r"\b(sword art online)\b",
                                                                                    message.content,
                                                                                    re.IGNORECASE) or re.search(
                r"\b(SAO)\b", message.content, re.IGNORECASE):
            if random.random() > 0.9:
                await message.channel.send("3/10")
                logger.log("reaction", f"Responded with '3/10' to message '{message.content}' from user {message.author.display_name}")

        # Imagine
        elif re.search(r"\b(imagine)\b", message.content, re.IGNORECASE) and random.random() > 0.9 and message.author.id != 569758271930368010:
            response = random.choice(["Imagine", "> i m a g i n e"])
            await message.channel.send(response)
            logger.log("reaction", f"Responded with '{response}' to message '{message.content}' from user {message.author.display_name}")

def setup(bot):
    bot.add_cog(Events(bot))
