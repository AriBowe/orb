import discord
from discord.ext import commands as bot_commands
import random
import csv
import re

COMMANDS_VERSION = {
    "version": "3",
    "count": "9"
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
    579281409403781131, # Test channel
    370068687782150144, # SMACK - Suggestions
    286411114969956352, # SMACK - General
    510668832403095575, # SMACK - Shitposting
    286460412415967233, # SMACK - Artdump
    287090586509377537, # SMACK - Musicdump
    286485013904621568, # SMACK - Memes
    510667650125398016, # SMACK - Uni-lyfe
    421260651038638096, # SMACK - Rood-n-Lood
    286460629215215618, # SMACK - Anime Manga General
    286460275496845312, # SMACK - Currently Screening
    286695380530495489, # SMACK - Spoiler City
    286460358695190529, # SMACK - Weeb Culture
    504537542797033472, # SMACK - Profiles and Such
    559348553214853130, # SMACK - SMACK Maid Cafe 2019
    286460137168961537, # SMACK - Vidyagames
    553588340516192266, # SMACK - Guild Wars 2 
    387159010861645824  # SMACK - Gacha Hell
]

PREFIX = "orb."

bot = bot_commands.Bot(command_prefix=PREFIX, help_command=None)

# Verifies if the command is allowed to be executed
# This is a utility function and shouldn't be called on it's own (hence the lack of .command decorator)
# Not async because a). Incredibly low complexity (aka fast)
#                   b). This is a priority to execute
#                   c). Nothing would be awaited in here so an async function would work the same as a regular
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

# Manual speaking
@bot.command()
async def say(ctx, channel, *, target=None):
    if ctx.author.id == 138198892968804352:
        if target == None:
            await ctx.send("Need a message")
        else:
            channel = bot.get_channel(int(channel))
            print("Sent message", str(target), "to channel", str(channel))
            await channel.send(target)

# New rank
# TODO: Add hard values to csv
@bot.command()
async def rank(ctx, *, target=None):
    if allowed_channel(ctx):
        with open("data/rank.csv", mode="r") as file:
            reader = csv.reader(file, delimiter=",")
            if target is None:
                await ctx.send("I can't rank nothing")
                return            
            elif re.match(r"(^|\s)me($|\s)", target, re.IGNORECASE):
                search_target = "<@" + str(ctx.author.id) + ">"
                target = "you"
            elif re.match(r"/(?=^.*" + str(ctx.author.display_name) + r".*$).*/gim", target, re.IGNORECASE) or re.match(r"(^|\s)" + str(ctx.author.id) + r"($|\s)", target, re.IGNORECASE):
                search_target = "<@" + str(ctx.author.id) + ">"
                target = "you"
            elif target.isnumeric():
                await ctx.send("I'd give " + target + " a " + target + " out of " + target)
            elif re.match(r"(^|\s)orb($|\s)", target, re.IGNORECASE) or re.match(r"(^|\s)<@569758271930368010>($|\s)", target, re.IGNORECASE):
                await ctx.send("I'd give me a 10 out of 10")
            else:
                search_target = target
            for line in reader:
                try:       
                    if re.match(r"(^|\s)" + str(search_target) + r"($|\s|.)", line[0], re.IGNORECASE):
                        await ctx.send("I'd give " + str(target) + " a " + str(line[1]) + " out of 10")
                        return
                except:
                    pass
        with open("data/rank.csv", mode="a") as file:
            writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)    
            random_value = str(random.randint(1,10))
            writer.writerow([str(search_target), random_value])
            await ctx.send("I'd give " + str(target) + " a " + str(random_value) + " out of 10")

# New BDE
# TODO: Code inital values
@bot.command()
async def bde(ctx, *, target=None):
    if allowed_channel(ctx):
        with open("data/bde.csv", mode="r") as file:
            reader = csv.reader(file, delimiter=",")
            if target is None:
                target = "the universe"
                search_target = "the universe"
            elif re.match(r"(^|\s)me($|\s)", target, re.IGNORECASE):
                search_target = "<@" + str(ctx.author.id) + ">"
                target = ctx.author.display_name
            elif re.match(r"/(?=^.*" + str(ctx.author.display_name) + r".*$).*/gim", target, re.IGNORECASE) or re.match(r"(^|\s)" + str(ctx.author.id) + r"($|\s)", target, re.IGNORECASE):
                search_target = "<@" + str(ctx.author.id) + ">"
                target = ctx.author.display_name
            elif re.match(r"(^|\s)orb($|\s)", target, re.IGNORECASE) or re.match(r"(^|\s)<@569758271930368010>($|\s)", target, re.IGNORECASE):
                await ctx.send("I have 101% bde")
            else:
                search_target = target
            for line in reader:
                try:       
                    if re.match(r"(^|\s)" + str(search_target) + r"($|\s|.)", line[0], re.IGNORECASE):
                        await ctx.send(str(target) + " has " + str(line[1]) + "% big dick energy")
                        return
                except:
                    pass
        with open("data/bde.csv", mode="a") as file:
            writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)    
            random_value = str(random.randint(0,100))
            writer.writerow([str(search_target), random_value])
            await ctx.send(str(target) + " has " + str(random_value) + "% big dick energy")

# Fishy
@bot.command()
async def fishy(ctx):
    if allowed_channel(ctx):
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
            elif re.match(r"(^|\s)me($|\s)", target, re.IGNORECASE):
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
        elif re.match(r"(^|\s)me($|\s)", target, re.IGNORECASE):
            await ctx.send(random.choice([("You're asking to be bullied? Isn't that kind of pathetic?"), ("You're a meanie!"), ("You're a dumb dumb")]), )
        else:
            await ctx.send(random.choice([("Bullying " + target), (target + " is a meanie!"), (target + " please stop speaking")]), )

# This will never get used mark my words
@bot.command()
async def fuckmeintheass(ctx):
    await ctx.add_reaction("🍆")

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
            await ctx.send(file=discord.File(fp="images/illya (" + str(random.randint(1, 40)) + ").png"))

# Slots
@bot.command()
async def slots(ctx, *, target=None):
    if allowed_channel(ctx):
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