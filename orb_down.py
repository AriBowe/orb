import discord
from discord.ext import commands
PREFIX = 'orb.'
VERSION_DATA = {
    "Chromatic": "Achromatic",
    "Version": 0,
    "Build": 0,
    "ChromaticHex": 0x000000
}
MESSAGE = discord.Game("Down for maintenance")
ONLINE_STATUS = "Down"
bot = commands.Bot(command_prefix=PREFIX, help_command=None)

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
    await ctx.send("Orb bot is a bot that does things.\nOrb is currently down for maintinence, however he should be back soon\nFor a list of commands see" + PREFIX + "commands. To check the bot status, see " + PREFIX + "status.\nDeveloped by xiii™#0013.")

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
