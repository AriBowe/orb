"""
Command expansion cog, handles all general commands
"""

import discord
from discord.ext import commands as bot_commands
import random
import csv
import re
import os
from google.cloud import firestore

from cogs.orb_control import allowed_channel, db

COMMANDS_VERSION = {
    "Version": "6",
    "Count": "13"
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
    "bde": ("Ranks your BDE", "Any input"),
    "translate": ("Translates your sentence into totally valid japanese", "Any input"),
    "gembutt": ("Posts gembutts (Houseki No Kuni characters)", "None"),
    "fatepost": ("Posts Fate series characters", "None"),
    "touhou": ("Posts Touhou characters", "None"),
    "yorimoi": ("Posts Yorimoi pictures", "None"),
    "kagepro": ("Posts images from the Kagerou Project", "None"),
    "vore": ("Says whether you vore people or get vored", "Any input"),
    "fight": ("Duel another user", "A valid user tag")
}

class CommandsCog(bot_commands.Cog):
    def __init__(self, bot):
        self.bot = bot
#         print("orb_commands loaded")

    # Allows generation and storage of user values (BDE, rank, and vore)
    def _generate_user_values(self, name: str):
        """
        Internal function. Generates random user values, stores them in the Firebase server, and then returns the new values. Does not check if the values already exist, use with caution.

        Arguments:
            name (str): The name to store the generated values under. Should be indentical to it's search_target designation

        Returns (dict): The generated values as a dictionary. Generated values are: BDE (int), ranking (int), and vore (bool)
        """
        data = {
            "bde": random.randint(1,100),
            "ranking": random.randint(1,10),
            "vore": bool(random.randint(0,1)),
        }

        # Store generated values
        db.collection('rankings').document(name).set(data)

        # Returns the generated values
        return data

    # Secreto
    @bot_commands.command()
    async def secret(self, ctx):
        """
        Easter egg command
        """
        if allowed_channel(ctx):
            print("Secret called. " + ctx.author.display_name + " is curious")
            await ctx.send(random.choice([":wink:", "Shhhh", ":thinking:"]))

    # Rank command
    @bot_commands.command(aliases=["rate"])
    async def rank(self, ctx, *, target=None):
        """
        Ranks a user on a scale of one to ten.
        """
        # Check if allowed channel
        if not allowed_channel(ctx):
            return

        print("Ranking", target, "for user", ctx.author.display_name, "(id", ctx.author.id, ")")        

        # Exceptions
        if target is None:
            await ctx.send("I can't rank nothing")
            return    
        elif re.match(r"(^|\s|.)@everyone($| $| .)", target, re.IGNORECASE):
            await ctx.send("I'm onto your schemes")
            return
        elif target.isnumeric():
            await ctx.send("I'd give " + target + " a(n) " + target + " out of " + target)
            return

        # Assign search target and displayed target
        if re.match(r"(^|\s|.)me($| $| .)", target, re.IGNORECASE):
            search_target = str(ctx.author.id)
            target = "you"
        elif re.match(r"/(?=^.*" + str(ctx.author.display_name) + r".*$).*/gim", target, re.IGNORECASE):
            search_target = str(ctx.author.id)
            target = "you"
        elif re.match(r"(<@|<@!)[0-9]+(>)", target, re.IGNORECASE):
            search_target = str(ctx.message.mentions[0].id)
        else:
            search_target = target

        # Load results
        doc_ref = db.collection(u'rankings').document(search_target)
        results = doc_ref.get().to_dict()

        if not results:
            results = self._generate_user_values(search_target)

        if target == 8 or target == 11:
            await ctx.send(f"I'd give {target} an {results['ranking']} out of 10")
        else:
            await ctx.send(f"I'd give {target} a {results['ranking']} out of 10")
            

    # Vore
    @bot_commands.command()
    async def vore(self, ctx, *, target=None):
        """
        Says if the user vores or gets vored
        """
        # Check if allowed channel
        if not allowed_channel(ctx):
            return

        print("Checking if", target, " is vored, for user", ctx.author.display_name, "(id", ctx.author.id, ")")        

        # Exceptions
        if target is None:
            await ctx.send("I can't vore nothing")
            return    
        elif re.match(r"(^|\s|.)@everyone($| $| .)", target, re.IGNORECASE):
            await ctx.send("I'm onto your schemes")
            return

        # Assign search target and displayed target
        if re.match(r"(^|\s|.)me($| $| .)", target, re.IGNORECASE):
            search_target = str(ctx.author.id)
            target = str(ctx.author.display_name)
        elif re.match(r"/(?=^.*" + str(ctx.author.display_name) + r".*$).*/gim", target, re.IGNORECASE) or re.match(r"(<@|<@!)[0-9]+(>)", target, re.IGNORECASE):
            search_target = str(ctx.author.id)
            target = str(ctx.author.display_name)
        elif re.match(r"(<@|<@!)[0-9]+(>)", target, re.IGNORECASE):
            search_target = str(ctx.message.mentions[0].id)
        else:
            search_target = target

        # Load results
        doc_ref = db.collection(u'rankings').document(search_target)
        results = doc_ref.get().to_dict()

        if not results:
            results = self._generate_user_values(search_target)

        if results["vore"] == "1":
            await ctx.send(str(target) + " vores")
        else:
            await ctx.send(str(target) + " gets vored")

    # BDE
    @bot_commands.command()
    async def bde(self, ctx, *, target=None):
        """
        Ranks the users BDE.
        """
        # Check if allowed channel
        if not allowed_channel(ctx):
            return

        print("BDE ranking", target, "for user", ctx.author.display_name, "(id", ctx.author.id, ")")        

        # Exceptions
        if target is None:
            await ctx.send("I can't rank the BDE of nothing")
            return    
        elif re.match(r"(^|\s|.)@everyone($| $| .)", target, re.IGNORECASE):
            await ctx.send("I'm onto your schemes")
            return

        # Assign search target and displayed target
        if re.match(r"(^|\s|.)me($| $| .)", target, re.IGNORECASE):
            search_target = str(ctx.author.id)
            target = str(ctx.author.display_name)
        elif re.match(r"/(?=^.*" + str(ctx.author.display_name) + r".*$).*/gim", target, re.IGNORECASE):
            search_target = str(ctx.author.id)
            target = str(ctx.author.display_name)
        elif re.match(r"(<@|<@!)[0-9]+(>)", target, re.IGNORECASE):
            search_target = str(ctx.message.mentions[0].id)
        else:
            search_target = target

        # Load results
        doc_ref = db.collection(u'rankings').document(search_target)
        results = doc_ref.get().to_dict()

        if not results:
            results = self._generate_user_values(search_target)

        await ctx.send(str(target) + "'s BDE is " + str(results["bde"]) + "%")

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

    # Gembutt
    @bot_commands.command()
    async def gembutt(self, ctx):
        if allowed_channel(ctx):
            print("Gembutt called by", ctx.author.display_name)
            await ctx.trigger_typing()
            await ctx.send(file=discord.File(fp="images/gembutt/gembutt (" + str(random.randint(1, 4)) + ").jpg"))

    # Kagepro
    @bot_commands.command()
    async def kagepro(self, ctx):
        if allowed_channel(ctx):
            print("Kagepro called by", ctx.author.display_name)
            await ctx.trigger_typing()
            await ctx.send(file=discord.File(fp="images/kagepro/kagepro (" + str(random.randint(1, 55)) + ").jpg"))

    # Yorimoi
    @bot_commands.command()
    async def yorimoi(self, ctx):
        if allowed_channel(ctx):
            print("Yorimoi called by", ctx.author.display_name)
            await ctx.trigger_typing()
            await ctx.send(file=discord.File(fp="images/yorimoi/yorimoi (" + str(random.randint(1, 48)) + ").jpg"))

    # Fatepost
    @bot_commands.command()
    async def fatepost(self, ctx):
        if allowed_channel(ctx):
            print("Fatepost called by", ctx.author.display_name)
            await ctx.trigger_typing()
            await ctx.send(file=discord.File(fp="images/fate/fatepost (" + str(random.randint(1, 56)) + ").jpg"))

    # Rinpost
    @bot_commands.command()
    async def rinpost(self, ctx):
        if allowed_channel(ctx):
            print("Rinpost called by", ctx.author.display_name)
            await ctx.trigger_typing()
            await ctx.send(file=discord.File(fp="images/rinpost/rin (" + str(random.randint(1, 46)) + ").jpg"))

    # Touhou
    @bot_commands.command()
    async def touhou(self, ctx):
        if allowed_channel(ctx):
            print("Touhou called by", ctx.author.display_name)
            await ctx.trigger_typing()
            await ctx.send(file=discord.File(fp="images/touhou/touhou (" + str(random.randint(1, 83)) + ").jpg"))

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

    # Translate - https://cdn.discordapp.com/attachments/286485013904621568/602745849650610177/FB_IMG_1563697773992.jpg
    @bot_commands.command()
    async def translate(self, ctx, *, target=None):
        TRANSLATE_DICT = {
        "a": "ka",
        "b": "tu",
        "c": "mi",
        "d": "te",
        "e": "ku",
        "f": "ru",
        "g": "ji",
        "h": "ri",
        "i": "ki",
        "j": "zu",
        "k": "me",
        "l": "ta",
        "m": "rin",
        "n": "to",
        "o": "mo",
        "p": "no",
        "q": "ke",
        "r": "shi",
        "s": "ari",
        "t": "chi",
        "u": "do",
        "v": "ru",
        "w": "mei",
        "x": "na",
        "y": "fu",
        "z": "zi"
        }
        
        if allowed_channel(ctx):
            output = ""
            print("Translating", target, "for", ctx.author.display_name)
            if target is None:
                await ctx.send(":thinking:")
            else:
                for char in target.lower():
                    try:
                        output += TRANSLATE_DICT[char]
                    except:
                        output += char

                translation = discord.Embed(description=str(output), colour=0xcb410b)
                translation.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

                await ctx.send(embed=translation)

def setup(bot):
    bot.add_cog(CommandsCog(bot))
