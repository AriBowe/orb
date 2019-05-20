import discord
from discord.ext import commands as bot_commands
import random

COMMANDS_VERSION = {
    "version": "3",
    "count": "8"
}

COMMAND_DATA = [
    ("help", "Displays help blurb", "None"), 
    ("commands", "Lists all commands", "None"), 
    ("ping", "Pings the bot, with various responses", "None"),
    ("ban", "'Bans' the user named (hint: doesn't work)", "Any input"),
    ("bully", "Bullies the user named", "Any input"),
    ("rank", "Ranks something", "Any input"),
    ("illya", "Posts Illya (weeb shit be warned)", "None"),
    ("bde", "Ranks your BDE", "Any input"),
    ("status", "Supplies info on orb's status", "None")
]

COMMAND_LIST = {
    "help": 0, 
    "commands": 1,
    "ping": 2,
    "ban": 3,
    "bully": 4, 
    "rank": 5,
    "illya": 6,
    "bde": 7,
    "status": 8,
}

BANNED_CHANNELS = [
    579281409403781131,
    370068687782150144,
    286411114969956352,
    510668832403095575,
    286460412415967233,
    287090586509377537,
    286485013904621568,
    510667650125398016,
    421260651038638096,
    286460629215215618,
    286460275496845312,
    286460275496845312,
    286695380530495489,
    286460358695190529,
    504537542797033472,
    559348553214853130,
    286460137168961537,
    553588340516192266,
    387159010861645824
]

PREFIX = "orb."

bot = bot_commands.Bot(command_prefix=PREFIX, help_command=None)

def allowed_channel(ctx):
    if ctx.message.channel.id in BANNED_CHANNELS:
        return False
    else:
        return True

# Secreto
@bot.command()
async def secret(ctx):
    if allowed_channel(ctx):
        print("Secret called. " + ctx.author.display_name + " is curious")
        await ctx.send(random.choice([":wink:", "Shhhh", ":thinking:"]))

# Fishy
@bot.command()
async def fishy(ctx):
    print("Fishing with", ctx.author.display_name)
    rand = random.randint(1,15)
    if rand <= 8:
        print("No catch")
        pass
    elif rand < 14:
        print("Not my job")
        await ctx.send(random.choice(["Not my job", "Wrong bot", ":thinking:"]))
    elif rand == 14:
        print("Caught wrench")
        await ctx.send(":fishing_pole_and_fish:  |  " + ctx.author.display_name + ", you caught: :wrench:! You paid :yen: 10 for casting.")
    else:
        print("Caught AIDS")
        await ctx.send(":fishing_pole_and_fish:  |  " + ctx.author.display_name + ", you caught: AIDS! You paid :yen: 10 for casting.")


# Meme ban
@bot.command()
async def ban(ctx, *, target=None):
    if allowed_channel(ctx):
        print("Ban on", target, "called for by", ctx.author.display_name)
        if random.randint(1, 5) == 1:
            await ctx.send("No")
        else:
            if target is None:
                await ctx.send(random.choice(["I can't ban nothing", "Specifiy a person please", "This command doesn't work like that"]))
            elif "ORB" in target.upper() or "<@569758271930368010>" in target or "ｏｒｂ" in target:
                await ctx.send("Pls no ban am good bot")
            elif "ME" in target.upper():
                await ctx.send("Banning you")
                await ctx.send("...")
                await ctx.send("Shit it didn't work")
            else:
                await ctx.send("Banning " + target)
                await ctx.send("...")
                await ctx.send("Shit it didn't work")

# Bully time
@bot.command()
async def bully(ctx, *, target=None):
    if allowed_channel(ctx):
        print("Bullying", target, "for", ctx.author.display_name)
        if target is None:
            await ctx.send("I can't bullly nothing")
        elif "NOTHING" in target.upper():
            await ctx.send("I can't bullly nothing")
        elif "ORB" in target.upper() or "<@569758271930368010>" in target:
            await ctx.send("No bulli :sadkot:")
        elif "ME" in target.upper():
            await ctx.send(random.choice([("You're asking to be bullied? Isn't that kind of pathetic?"), ("You're a meanie!"), ("You're a dumb dumb"), ]), )
        else:
            await ctx.send(random.choice([("Bullying " + target), (target + " is a meanie!"), (target + " please stop speaking")]), )

# Ranking
@bot.command()
async def rank(ctx, *, target=None):
    if allowed_channel(ctx):
        print("Ranking", target, "for", ctx.author.display_name)
        if target is None:
            await ctx.send("I can't rank nothing")
        elif "ORB" in target.upper() or "<@569758271930368010>" in target:
            await ctx.send("I'd give me a 10 out of 10")
        elif "ME" in target.upper():
            await ctx.send("I'd give you a " + str(random.randint(0, 10)) + " out of 10")
        elif "NEKO" in target.upper():
            if random.randint(1, 10) == 10:
                await ctx.send("EZ 10 tbh")
            else:
                await ctx.send("I'd give " + target + " a " + str(random.randint(7, 10)) + " out of 10")
        elif target.isnumeric():
            await ctx.send("I'd give " + target + " a " + target + " out of " + target)
        else:
            await ctx.send("I'd give " + target + " a " + str(random.randint(0, 10)) + " out of 10")

# Illya
@bot.command()
async def illya(ctx):
    if allowed_channel(ctx):
        print("Illya called by", ctx.author.display_name)
        if random.randint(1, 50) == 2:
            await ctx.trigger_typing()
            await ctx.send(file=discord.File(fp="images/lolice.gif"))
        else:
            await ctx.trigger_typing()
            await ctx.send(file=discord.File(fp="images/illya_" + str(random.randint(1, 11)) + ".png"))

# BDE
@bot.command()
async def bde(ctx, *, target=None):
    if allowed_channel(ctx):
        print("BDE called by", ctx.author.display_name)
        if target is None:
            await ctx.send("The universe has " + str(random.randint(0,100)) + "% dick energy")
        elif "ORB" in target.upper() or "<@569758271930368010>" in target:
            await ctx.send("I have 101% dick energy")
        elif "ME" in target.upper():
            await ctx.send("You have " + str(random.randint(0,100)) + "% dick energy")
        else:
            await ctx.send(target + " has " + str(random.randint(0,100)) + "% dick energy")

# Slots
@bot.command()
async def slots(ctx, *, target=None):
    if target is not None and target.isnumeric():
        await ctx.send("""[  :slot_machine: l SLOTS ]
------------------
:banana: : :banana: : :banana:

:regional_indicator_g: :regional_indicator_a: :regional_indicator_y:  <

:flag_lv: : :tangerine: : :watermelon:
------------------
| : : :  LOST  : : : |

**""" + ctx.author.display_name + "** used **" + target + "** credit(s) and got the big gay")
    else:
        await ctx.send("""[  :slot_machine: l SLOTS ]
------------------
:banana: : :banana: : :banana:

:regional_indicator_g: : :regional_indicator_a: : :regional_indicator_y:  <

:flag_lv: : :tangerine: : :watermelon:
------------------
| : : :  LOST  : : : |

**""" + ctx.author.display_name + "** used **1** credit(s) and got the big gay")