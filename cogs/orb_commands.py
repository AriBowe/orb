import discord
from discord.ext import commands as bot_commands
import random
import csv
import re

from cogs.orb_control import allowed_channel

COMMANDS_VERSION = {
    "Version": "3",
    "Count": "9"
}

# PUBLIC list of commands, not all of them
COMMAND_DATA = {
    "ping": ("Pings the bot, with various responses", "None"),
    "help": ("Displays help blurb", "None"), 
    "status": ("Supplies info on orb's status", "None"),
    "commands": ("Lists all commands", "Any command name, or all"), 
    
    "ban": ("'Bans' the user named (hint: doesn't work)", "Any input"),
    "bully": ("Bullies the user named", "Any input"),
    "rank": ("Ranks something", "Any input"),
    "illya": ("Posts Illya (weeb shit be warned)", "None"),
    "bde": ("Ranks your BDE", "Any input")
}

class CommandsCog(bot_commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("orb_commands loaded")

    # Secreto
    @bot_commands.command()
    async def secret(self, ctx):
        if allowed_channel(ctx):
            print("Secret called. " + ctx.author.display_name + " is curious")
            await ctx.send(random.choice([":wink:", "Shhhh", ":thinking:"]))

    # New rank
    @bot_commands.command(aliases=["rate"])
    async def rank(self, ctx, *, target=None):
        if allowed_channel(ctx):
            print("Ranking", target, "for user", ctx.author.display_name, "id", ctx.author.id)
            with open("data/rank.csv", mode="r", newline="") as file:
                reader = csv.reader(file, delimiter=",")
                if target is None:
                    await ctx.send("I can't rank nothing")
                    return    
                elif re.match(r"(^|\s|.)@everyone($| $| .)", target, re.IGNORECASE):
                    return
                elif re.match(r"(^|\s|.)me($| $| .)", target, re.IGNORECASE):
                    search_target = "<@" + str(ctx.author.id) + ">"
                    target = "you"
                elif re.match(r"/(?=^.*" + str(ctx.author.display_name) + r".*$).*/gim", target, re.IGNORECASE) or re.match(r"(^|\s|.)" + str(ctx.author.id) + r"($| $| .)", target, re.IGNORECASE):
                    search_target = "<@" + str(ctx.author.id) + ">"
                    target = "you"
                elif target.isnumeric():
                    await ctx.send("I'd give " + target + " a " + target + " out of " + target)
                elif re.match(r"(^|\s|.)orb($| $| .)", target, re.IGNORECASE) or re.match(r"(^|\s|.)<@569758271930368010>($| $| .)", target, re.IGNORECASE):
                    await ctx.send("I'd give me a 10 out of 10")
                    return
                else:
                    search_target = target
                for line in reader:
                    try:       
                        if re.match(r"(^|\s|.)" + str(search_target) + r"($)", line[0], re.IGNORECASE):
                            await ctx.send("I'd give " + str(target) + " a " + str(line[1]) + " out of 10")
                            return
                    except:
                        pass
            with open("data/rank.csv", mode="a", newline="") as file:
                writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)    
                random_value = str(random.randint(1,10))
                writer.writerow([str(search_target), random_value])
                await ctx.send("I'd give " + str(target) + " a " + str(random_value) + " out of 10")

    # New BDE
    @bot_commands.command()
    async def bde(self, ctx, *, target=None):
        if allowed_channel(ctx):
            print("BDEing " + target + " for " + ctx.author.display_name)
            with open("data/bde.csv", mode="r", newline="") as file:
                reader = csv.reader(file, delimiter=",")
                if target is None:
                    target = "the universe"
                    search_target = "the universe"
                elif re.match(r"(^|\s|.)@everyone($| $| .)", target, re.IGNORECASE):
                    return
                elif re.match(r"(^|\s|.)me($| $| .)", target, re.IGNORECASE):
                    search_target = "<@" + str(ctx.author.id) + ">"
                    target = ctx.author.display_name
                elif re.match(r"/(?=^.*" + str(ctx.author.display_name) + r".*$).*/gim", target, re.IGNORECASE) or re.match(r"(^|\s|.)" + str(ctx.author.id) + r"($| $| .)", target, re.IGNORECASE):
                    search_target = "<@" + str(ctx.author.id) + ">"
                    target = ctx.author.display_name
                elif re.match(r"(^|\s|.)orb($| $| .)", target, re.IGNORECASE) or re.match(r"(^|\s|.)<@569758271930368010>($| $| .)", target, re.IGNORECASE):
                    await ctx.send("I have 101% bde")
                    return
                else:
                    search_target = target
                for line in reader:
                    try:       
                        if re.match(r"(^|\s|.)" + str(search_target) + r"($| $| .|.)", line[0], re.IGNORECASE):
                            await ctx.send(str(target) + " has " + str(line[1]) + "% big dick energy")
                            return
                    except:
                        pass
            with open("data/bde.csv", mode="a", newline="") as file:
                writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)    
                random_value = str(random.randint(0,100))
                writer.writerow([str(search_target), random_value])
                await ctx.send(str(target) + " has " + str(random_value) + "% big dick energy")

    # Fishy
    @bot_commands.command()
    async def fishy(self, ctx):
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
    @bot_commands.command()
    async def ban(self, ctx, *, target=None):
        if allowed_channel(ctx):
            print("Ban on", target, "called for by", ctx.author.display_name)
            if random.randint(1, 5) == 1:
                await ctx.send("No")
            else:
                if target is None:
                    await ctx.send(random.choice(["I can't ban nothing", "Specifiy a person please", "This command doesn't work like that"]))
                elif re.match(r"(^|\s|.)@everyone($| $| .)", target, re.IGNORECASE):
                    return
                elif "ORB" in target.upper() or "<@569758271930368010>" in target or "ｏｒｂ" in target:
                    await ctx.send("Pls no ban am good bot")
                elif re.match(r"(^|\s|.)me($| $| .)", target, re.IGNORECASE):
                    await ctx.send("Banning you")
                    await ctx.send("...")
                    await ctx.send("Shit it didn't work")
                else:
                    await ctx.send("Banning " + target)
                    await ctx.send("...")
                    await ctx.send("Shit it didn't work")

    # Bully time
    @bot_commands.command()
    async def bully(self, ctx, *, target=None):
        if allowed_channel(ctx):
            print("Bullying", target, "for", ctx.author.display_name)
            if target is None:
                await ctx.send("I can't bully nothing")
            elif re.match(r"(^|\s|.)nothing($| $| .)", target, re.IGNORECASE):
                await ctx.send("I can't bully nothing")
            elif re.match(r"(^|\s|.)orb($| $| .)", target, re.IGNORECASE) or re.match(r"(^|\s|.)<@569758271930368010>($| $| .)", target, re.IGNORECASE):
                await ctx.send("No bulli :sadkot:")
            elif re.match(r"(^|\s|.)me($| $| .)", target, re.IGNORECASE):
                await ctx.send(random.choice([("You're asking to be bullied? Isn't that kind of pathetic?"), ("You're a meanie!"), ("You're a dumb dumb")]), )
            else:
                await ctx.send(random.choice([("Bullying " + target), (target + " is a meanie!"), (target + " please stop speaking")]), )

    # This will never get used mark my words
    @bot_commands.command()
    async def fuckmeintheass(self, ctx):
        await ctx.add_reaction("🍆")

    # Illya
    @bot_commands.command()
    async def illya(self, ctx):
        if allowed_channel(ctx):
            print("Illya called by", ctx.author.display_name)
            if random.randint(1, 50) == 2:
                await ctx.trigger_typing()
                await ctx.send(file=discord.File(fp="images/lolice.gif"))
            else:
                await ctx.trigger_typing()
                await ctx.send(file=discord.File(fp="images/illya/illya (" + str(random.randint(1, 47)) + ").jpg"))

    # Slots
    @bot_commands.command()
    async def slots(self, ctx, *, target=None):
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

def setup(bot):
    bot.add_cog(CommandsCog(bot))