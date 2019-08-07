import discord
from discord.ext import commands

# Get prefixes
def get_prefix(bot, message):
    PREFIXES = ["orb.", "o."]
    return bot_commands.when_mentioned_or(*PREFIXES)(bot, message)

# Imports libraries needed
import discord
from discord.ext import commands as bot_commands
print("Base libraries successfully loaded")

# Assigns bot & client
bot = bot_commands.Bot(command_prefix=get_prefix, help_command=None, case_insensitive=True)
client = discord.Client()

# Assigns constants
VERSION_DATA = {
    "Chromatic": "Achromatic",
    "Version": 0,
    "Build": 0,
    "ChromaticHex": 0x000000
}
MESSAGE = discord.Game("Down for maintenance")
ONLINE_STATUS = "Down"
bot = commands.Bot(command_prefix=get_prefix, help_command=None)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.dnd, activity=MESSAGE)

# Ping
@bot.command()
async def ping(ctx):
    # print("Ping received from", discord.Message.author.display_name)
    await ctx.send("Ping received")


# Orb bot help text
@bot.command()
async def help(ctx):
    # print("Help request received from", message.author.display_name)
    await ctx.send("Orb bot is a bot that does things.\nOrb is currently down for maintinence, however he should be back soon\nFor a list of commands see orb.commands. To check the bot status, see orb.status.\nDeveloped by xiii™#0013.")

# Status
@bot.command()
async def status(ctx):
    # print("Status requested from", message.author.display_name)
    embed=discord.Embed(title="", color=VERSION_DATA["ChromaticHex"])
    embed.set_author(name="ORB STATUS")
    embed.add_field(name="Colour", value=VERSION_DATA["Chromatic"], inline=True)
    embed.add_field(name="Version", value=VERSION_DATA["Version"], inline=True)
    embed.add_field(name="Build", value=VERSION_DATA["Build"], inline=True)
    embed.add_field(name="Online Status", value=ONLINE_STATUS, inline=False)
    await ctx.send(embed=embed)

bot.run("no")
