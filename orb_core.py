"""
Use the following link to add the bot:
https://discordapp.com/oauth2/authorize?client_id=569758271930368010&scope=bot&permissions=64
"""

# Get prefixes
def get_prefix(bot, message):
    PREFIXES = ["orb.", "o."]
    return bot_commands.when_mentioned_or(*PREFIXES)(bot, message)

# Imports libraries needed
import discord
from discord.ext import commands as bot_commands
import random
import os
import csv
import re
import sys
print("Base libraries successfully loaded")

# Gets constants from files. Yay interlinking
from cogs.orb_commands import COMMANDS_VERSION, COMMAND_DATA
from cogs.orb_control import BANNED_CHANNELS, allowed_channel

# Assigns bot & client
bot = bot_commands.Bot(command_prefix=get_prefix, help_command=None, case_insensitive=True)
client = discord.Client()

# Assigns constants
MESSAGE = discord.Game("with orbs. Try orb.help")
VERSION_DATA = {
    "Colour": "Sinopia",
    "Version": 7,
    "Build": 2,
    "ColourHex": 0xcb410b
}
ONLINE_STATUS = "Online"

# List of extensions
INITIAL_EXTENSIONS = [
    "cogs.orb_commands",\
    "cogs.orb_control",
    # "cogs.orb_economy"
]

# Imports extensions
if __name__ == '__main__':
    for extension in INITIAL_EXTENSIONS:
        bot.load_extension(extension)



# Displays boot complete message
@bot.event
async def on_ready():
    with open("data/banned_channels.csv", mode="r") as file:
        reader = csv.reader(file, delimiter=",")
        for line in reader:
            try:
                BANNED_CHANNELS.append(int(line[0]))
            except:
                pass
    await bot.change_presence(status=discord.Status.online, activity=MESSAGE)
    print("\nORB Core", VERSION_DATA["Colour"], VERSION_DATA["Version"], "Build", VERSION_DATA["Build"])
    print('Bot startup successful. Logged in as {0.user}'.format(bot))

# Ping
@bot.command()
async def ping(ctx):
    if allowed_channel(ctx):
        print("Ping received from", ctx.author.display_name)
        await ctx.send(random.choice(["Hello!", "Ping!", "Ping received", "Pong!"]))


# Orb bot help text
@bot.command()
async def help(ctx):
    if allowed_channel(ctx):
        print("Help request received from", ctx.author.display_name)
        await ctx.send("Orb bot is a bot that does things. Features include:\n   - Reactions\n   - Posting Illya\n   - Ranking\nFor a list of commands see orb.commands, or check them out online at https://aribowe.github.io/orb/commands. To check the bot status, see orb.status.\nDeveloped by xiii™#0013.")

# Status
@bot.command()
async def status(ctx):
    if allowed_channel(ctx):
        print("Status requested from", ctx.author.display_name)
        embed=discord.Embed(title="", color=VERSION_DATA["ColourHex"])
        embed.set_author(name="ORB STATUS")
        embed.add_field(name="Core Version", value=VERSION_DATA["Version"], inline=True)
        embed.add_field(name="Core Build", value=VERSION_DATA["Build"], inline=True)
        embed.add_field(name="Commands Version", value=COMMANDS_VERSION["Version"], inline=True)
        embed.add_field(name="Online Status", value=ONLINE_STATUS, inline=False)
        await ctx.send(embed=embed)

# Lists commands
@bot.command()
async def commands(ctx, target=None):
    if allowed_channel(ctx):
        output = ""
        if target is None:
            print("Command overview requested from", ctx.author.display_name)
            output += "**Accepted commands:**\n```"
            for command in COMMAND_DATA:
                output += "orb." + command + "\n"
            output += "```\n```Call a specific command for more info, or all for a full command dump```"
        elif target.upper() == "ALL":
            print("Full commands list requested from", ctx.author.display_name)
            for command in COMMAND_DATA:
                output += "```Command: " + "orb." + command + "\n"
                output += "Function: " + COMMAND_DATA[command][0] + "\n"
                output += "Arguments: " + COMMAND_DATA[command][1] + "```"
        else:
            print("Info on " + target + " requested by " + ctx.author.display_name)

            info, args = COMMAND_DATA[target]
            output += "```Command: orb." + target + "\n"
            output += "Function: " + str(info) + "\n"
            output += "Arguments: " + str(args) + "```"
            # except:
            #     print("Command not found")
            #     output = "Error: Command not found"
        await ctx.send(output)

@bot.event
async def on_message(message):
    # If message contains very cool, or otherwise a 1/2000 chance of reacting "very cool"
    if re.match(r"(^|\s|.)very cool($| $| .)", message.content, re.IGNORECASE) or random.randint(1, 2000) == 1:
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
    elif re.match(r"(^|\s|.)girl[']s? aren[']?t real($| $| .)", message.content, re.IGNORECASE):
        rand_int = random.randint(1, 10)
        print("Not real")
        if rand_int <= 3:
            await message.add_reaction("🇹")
            await message.add_reaction("🇷")
            await message.add_reaction("🇺")
            await message.add_reaction("🇪")
            print("Reacted 'true' to the message", "'" + message.content + "'", "from user", message.author.display_name)
        elif rand_int > 3 and rand_int <= 5:
            print("Ignored", "'" + message.content + "'", "from user", message.author.display_name)
            pass
        else:
            await message.add_reaction("🇫")
            await message.add_reaction("🇦")
            await message.add_reaction("🇨")
            await message.add_reaction("🇹")
            print("Reacted 'fact' to the message", "'" + message.content + "'", "from user", message.author.display_name)

    # Epic reaction time
    elif re.match(r"(^|\s|.)epic($| $| .)", message.content, re.IGNORECASE):
        if random.randint(1, 15) == 1:
            await message.add_reaction("🇪")
            await message.add_reaction("🅱")
            await message.add_reaction("🇮")
            await message.add_reaction("🇨")
            print("Reacted 'ebic' to the message", "'" + message.content + "'", "from user", message.author.display_name)
        else:
            await message.add_reaction("🇪")
            await message.add_reaction("🇵")
            await message.add_reaction("🇮")
            await message.add_reaction("🇨")
            print("Reacted 'epic' to the message", "'" + message.content + "'", "from user", message.author.display_name)

    # Big guy react
    elif re.match(r"(^)big guy($| $| .)", message.content, re.IGNORECASE):
        await message.channel.send("For you")

    # Awoo react
    elif re.match(r"(^|\s|.)awoo($| $| .)", message.content, re.IGNORECASE):
        await message.add_reaction("🇦")
        await message.add_reaction("🇼")
        await message.add_reaction("🇴")
        await message.add_reaction("🅾")
        
    else:
        await bot.process_commands(message)

bot.run(os.environ['DISCORD_TOKEN'], bot=True, reconnect=True)