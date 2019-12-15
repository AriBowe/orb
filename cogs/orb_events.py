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
from utils import repo


async def send_command_help(ctx):
    """
    Sends help message for specific command

    Params:
        (discord.ext.commands.Context) ctx: context
    """
    if ctx.invoked_subcommand:
        _help = await ctx.bot.formatter.format_help_for(ctx, ctx.invoked_subcommand)
    else:
        _help = await ctx.bot.formatter.format_help_for(ctx, ctx.command)

    for page in _help:
        await ctx.send(page)

class Events(bot_commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        VERSION_DATA = {
            "Colour": "Sinopia",
            "Version": 7,
            "Build": 4,
            "ColourHex": 0xcb410b
        }

    # Displays boot complete message
    async def on_ready(self):
        if not hasattr(self.bot, 'uptime'):
            self.bot.uptime = datetime.datetime.now()
        # Assigns constants
        MESSAGE = discord.Game("with orbs. Try orb.help")
        VERSION_DATA = {
            "Colour": "Sinopia",
            "Version": 7,
            "Build": 4,
            "ColourHex": 0xcb410b
        }

        with open("data/banned_channels.csv", mode="r") as file:
            reader = csv.reader(file, delimiter=",")
            for line in reader:
                try:
                    BANNED_CHANNELS.append(int(line[0]))
                except:
                    pass

        await self.bot.change_presence(status=discord.Status.online, activity=MESSAGE)
        print("\nORB Core", VERSION_DATA["Colour"], VERSION_DATA["Version"], "Build", VERSION_DATA["Build"])
        print('------------------------------------------')
        print('Bot is online and connected to Discord.')
        print(f'Currently connected to {len(self.bot.guilds)} server.' if len(self.bot.guilds) == 1
              else f'Currently Connected to {len(self.bot.guilds)} servers.')
        print('------------------------------------------')
        print('Bot Name: ' + self.bot.user.name)
        print('Bot ID: ' + str(self.bot.user.id))
        print('')
        print('Discord.py Version: ' + discord.__version__)
        print('Python Version: ' + sys.version[:5])
        print('')
        print('orb.py Version: ' + VERSION_DATA["Version"])
        print('------------------------------------------')


    async def on_command_error(self, ctx, error: errors):
        """
        Bot posts message when command errors occur

        Params:
            (discord.ext.commands.Context) ctx: Context
            (discord.ext.commands.errors): errors
        """
        if isinstance(error, errors.CommandNotFound):
            await ctx.send(f'Invalid command. Please type `{repo.get_prefix}help` to see a list of commands.')

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

    async def on_command(self, ctx):
        """Prints user commands to console"""
        try:
            print(f'{ctx.guild.me} > {ctx.message.channel} > {ctx.message.author.name} > {ctx.message.clean_content}')
        except AttributeError:
            print(f'Private Message > {ctx.message.channel} > {ctx.message.author.name} > {ctx.message.clean_content}')


    async def on_message(self, message):
        # If message contains very cool, or otherwise a 1/2000 chance of reacting "very cool"
        if (re.search(r"\b(very cool)\b", message.content, re.IGNORECASE) and random.random > 0.5) or random.randint(1,
                                                                                                                     2000) == 1:
            await message.add_reaction("🇻")
            await message.add_reaction("🇪")
            await message.add_reaction("🇷")
            await message.add_reaction("🇾")
            await message.add_reaction("🇨")
            await message.add_reaction("🇴")
            await message.add_reaction("🅾")
            await message.add_reaction("🇱")
            print("Reacted 'very cool' to message", "'" + message.content + "'", "from user", message.author.display_name)

        # Girls aren't real
        elif re.search(r"\b(girl[']?s aren[']?t real)\b", message.content, re.IGNORECASE):
            rand_int = random.randint(1, 10)
            print("Not real")
            if rand_int <= 3:
                await message.add_reaction("🇹")
                await message.add_reaction("🇷")
                await message.add_reaction("🇺")
                await message.add_reaction("🇪")
                print("Reacted 'true' to the message", "'" + message.content + "'", "from user",
                      message.author.display_name)
            elif rand_int > 3 and rand_int <= 5:
                print("Ignored", "'" + message.content + "'", "from user", message.author.display_name)
                pass
            else:
                await message.add_reaction("🇫")
                await message.add_reaction("🇦")
                await message.add_reaction("🇨")
                await message.add_reaction("🇹")
                print("Reacted 'fact' to the message", "'" + message.content + "'", "from user",
                      message.author.display_name)

        # Epic reaction time
        elif re.search(r"\b(epic)\b", message.content, re.IGNORECASE) and random.random > 0.5:
            if random.randint(1, 15) == 1:
                await message.add_reaction("🇪")
                await message.add_reaction("🅱")
                await message.add_reaction("🇮")
                await message.add_reaction("🇨")
                print("Reacted 'ebic' to the message", "'" + message.content + "'", "from user",
                      message.author.display_name)
            else:
                await message.add_reaction("🇪")
                await message.add_reaction("🇵")
                await message.add_reaction("🇮")
                await message.add_reaction("🇨")
                print("Reacted 'epic' to the message", "'" + message.content + "'", "from user",
                      message.author.display_name)

        # Big guy react
        elif re.search(r"\b(big guy)\b", message.content, re.IGNORECASE) and random.random > 0.75:
            await message.channel.send("For you")
            print("Responded with 'For you' to message '" + message.content + "' from user " + message.author.display_name)

        # Awoo react
        elif re.search(r"\b(awoo+)\b", message.content, re.IGNORECASE):
            await message.add_reaction("🇦")
            await message.add_reaction("🇼")
            await message.add_reaction("🇴")
            await message.add_reaction("🅾")
            print("Reacted with 'awoo' to message '" + message.content + "' from user " + message.author.display_name)

        # 3/10
        elif re.search(r"\b(asuna)\b", message.content, re.IGNORECASE) or re.search(r"\b(sword art online)\b",
                                                                                    message.content,
                                                                                    re.IGNORECASE) or re.search(
                r"\b(SAO)\b", message.content, re.IGNORECASE):
            if random.random() > 0.9:
                await message.channel.send("3/10")
                print("Responded with '3/10' to message '" + message.content + "' from user " + message.author.display_name)

        # Imagine
        elif re.search(r"\b(imagine)\b", message.content, re.IGNORECASE) and random.random() > 0.9:
            await message.channel.send(random.choice(["Imagine", "> i m a g i n e"]))

            # # 40 kg
            # elif re.search(r"\b(40[ ]?kg)\b", message.content, re.IGNORECASE) and random.random() > 0.95:
            #     await message.channel.send(random.choice(["145 cm", "I M A G I N E"]))

            # # Roughly 145 cm
            # elif re.search(r"\b(145[ ]?cm)\b", message.content, re.IGNORECASE) and random.random() > 0.99:
            #     await message.channel.send(random.choice(["40 kg", "I M A G I N E", "Imagine how fun it would be to manhandle her tiny body"]))

            # elif re.search(r"\b(imagine)\b", message.content, re.IGNORECASE) and random.randint(1,1000) == 420:
            #     await message.channel.send("https://i.kym-cdn.com/photos/images/newsfeed/001/455/798/54e.jpg")

            # Level up
        elif re.search(r"(leveled up!)", message.content, re.IGNORECASE) and message.author.id == 172002275412279296:
            await message.add_reaction("🇬")
            await message.add_reaction("🇿")

            # OwO
        elif re.search(r"\b(owo)\b", message.content, re.IGNORECASE):
            await message.add_reaction("🇴")
            await message.add_reaction("🇼")
            await message.add_reaction("🅾")

            # Data are is the wrong way to say it
        elif re.search(r"\b(data are)\b", message.content, re.IGNORECASE):
            await message.add_reaction(bot.get_emoji(415384489733128195))

            # Orb
        elif re.search(r"(\b|:)(orb)(\b|:|^.)", message.content, re.IGNORECASE) and random.random > 0.99:
            await message.add_reaction(bot.get_emoji(587198415348170773))

            # # Gay
            # elif re.search(r"\b(gays)\b", message.content, re.IGNORECASE) and random.random > 0.99:
            #     await message.add_reaction("🇬")
            #     await message.add_reaction("🇦")
            #     await message.add_reaction("🇾")
        #
        # await bot.process_commands(message)

def setup(bot):
    bot.add_cog(Events(bot))
