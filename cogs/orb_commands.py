"""
Command expansion cog, handles all general commands
"""

import discord
import asyncio
from discord.ext import commands as bot_commands
import random
import time
import csv
import re
import os
import requests
from datetime import date, datetime
from google.cloud import firestore
from bs4 import BeautifulSoup
from mcstatus import JavaServer
import math

from cogs.orb_control import allowed_channel, db
from utils.repo import SMACKCRAFT

COMMANDS_VERSION = {
    "Version": "10",
    "Count": "28"
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
    "fight": ("Duel another user", "A valid user tag"),
    "nimble": ("Posts horses. Lots of horses.", "None"),
    "haze": ("Tells Haze to do his assignment", "None"),
    "pablo": ("Posts Pablo's flamingos", "None"),
    "dad": ("Hi x, I'm y joke", "Any input"),
    "azsry": ("Posts a programming meme", "None"),
    "covid": ("Posts most recent COVID-19 data for Australia from Qld Health", "None"),
    "gundam": ("Posts the 'watch gundam!' image", "None"),
    "nido": ("Sends out one of his personal phrases", "None"),
    "salty": ("Posts a picture of some salt implying it is you", "None")
}


class CommandsCog(bot_commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Allows generation and storage of user values (BDE, rank, and vore)
    def _generate_user_values(self, name: str):
        """
        Internal function. Generates random user values, stores them in the Firebase server, and then returns the new values. Does not check if the values already exist, use with caution.

        Arguments:
            name (str): The name to store the generated values under. Should be indentical to it's search_target designation

        Returns (dict): The generated values as a dictionary. Generated values are: BDE (int), ranking (int), and vore (bool)
        """
        data = {
            "bde": random.randint(1, 100),
            "ranking": random.randint(1, 10),
            "vore": bool(random.randint(0, 1)),
        }

        # Store generated values
        db.collection('rankings').document(name).set(data)

        # Returns the generated values
        return data

    async def get_image(self):
        pass

    # Secreto
    @bot_commands.command()
    async def secret(self, ctx):
        """
        Easter egg command
        """
        if allowed_channel(ctx):
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
            rand = random.randint(1, 15)
            if rand <= 8:
                pass
            elif rand < 14:
                await ctx.send(random.choice(["Not my job", "Wrong bot", ":thinking:"]))
            elif rand == 14:
                await ctx.send(":fishing_pole_and_fish:  |  " + ctx.author.display_name + ", you caught: :wrench:! You paid :yen: 10 for casting.")
            else:
                await ctx.send(":fishing_pole_and_fish:  |  " + ctx.author.display_name + ", you caught: AIDS! You paid :yen: 10 for casting.")

    # Meme ban
    @bot_commands.command()
    async def ban(self, ctx, *, target=None):
        if allowed_channel(ctx):
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

    # Commands
    @bot_commands.command()
    async def commands(self, ctx):
        if allowed_channel(ctx):
            await ctx.trigger_typing()

            command_list = ""
            for key in COMMAND_DATA.keys():
                explanation, inputReq = COMMAND_DATA[key]

                output = "**{}** | {}".format(key, explanation)
                if (inputReq != "None"):
                    output += " << *{}*".format(inputReq)

                command_list += output+"\n"

            await ctx.send(command_list)

    # Nido
    @bot_commands.command()
    async def nido(self, ctx, explain=None):
        if allowed_channel(ctx):
            await ctx.trigger_typing()
            phrases = ["Grime is better than Kpop", "Honda Odyssey best car", "We live in a society", "Haze needs to do his assignment",
                       "Initial D best anime", "If Honda made a manuelle Odyssey in brown there would be no need for any other cars",
                       "Northside is a cult", "The C in SMACK stands for \"corrupt\""]

            # punishment for pinning a message that misquoted what I had said about #humans and #onis (Nidowott#4381)
            if (("I <3 humans" not in ctx.author.display_name) and str(ctx.author) == "Nidowott#4381"):
                if (explain != "explain"):
                    current = datetime.now()
                    # randomly decides whether or not to apply karma to the message
                    if (random.randint(0, 10) >= 5 or current.strftime("%a") == "Fri"):
                        await ctx.send("(-1) **Karma** - after pinning that image of my sponsorship, your command will be cursed.")
                    else:
                        await ctx.send(random.choice(phrases))
                else:
                    # explanation of the chances
                    await ctx.trigger_typing()
                    await ctx.send("It's quite simple really.")
                    await asyncio.sleep(0.5)
                    await ctx.send("> - It picks a random number from 0 to 10. Whenever it is greater than 4, you get the curse.")
                    await ctx.send("> - If the day is Friday, you will always get the curse. You don't get to enjoy Fridays.")
                    await asyncio.sleep(0.5)
                    await ctx.send("\nHave fun! :smile:\n- Pablo\nP.S Come and talk if you want to exorcise your command :wink:")
            else:
                await ctx.send(random.choice(phrases))

    # Salty
    @bot_commands.command()
    async def salty(self, ctx):
        if allowed_channel(ctx):
            await ctx.trigger_typing()
            await ctx.send(file=discord.File(fp="images/salty.jpeg"))

    @bot_commands.command(aliases=["mc"])
    async def smackcraft(self, ctx):
        if allowed_channel(ctx):
            smckcrft = JavaServer.lookup(SMACKCRAFT) # move this to config later

            try:
                status = smckcrft.status()
                embed = discord.Embed(title="SMACKcraft", description=status.description, color=0x287233)
                embed.add_field(name="Active Players:", value=str(status.players.online))
                embed.add_field(name="Version:", value=str(status.version.name))
                embed.add_field(name="Latency:", value=round(status.latency, 2))

                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send("An error was encountered when trying to query the server. Is it offline?")

    # Dev
    @bot_commands.command()
    async def dev(self, ctx, cmd=None):
        if allowed_channel(ctx):
            await ctx.trigger_typing()
            if not cmd:
                await ctx.send('Please choose one of the following arguments:\n*follow*\t*unfollow*')
                return

            # check with command they would like to execute
            id = ctx.author.id
            if cmd in ['follow', 'Follow']:
                # write their ID to the file as a new line
                followers = open('data/followers.txt', 'w')
                followers.write(str(id) + '\n')
                followers.close()
                await ctx.send('You are now following orb updates!')

            elif cmd in ['unfollow', 'Unfollow']:
                lines = []
                #followers = open('data/followers.txt', 'w')

                with open('data/followers.txt', 'r') as f:
                    lines = f.readlines()

                with open('data/followers.txt', 'w') as f:
                    for line in lines:
                        # if " " in line:
                        # print(True)

                        #print(line.strip(), type(line.strip()))
                        #print(id, type(id))

                        if (line.strip() != str(id)):
                            f.write(line)

                    '''for line in range(len(lines)):
                        lineId = lines[line][0:-1]
                        lines[line].replace(str(id), '')'''

                    '''if lineId == id:
                            # a match has been found, remove it
                            followers.truncate(size)
                            size -= len(line)'''

                # followers.close()

                await ctx.send('You are no longer following orb updates!')
                # await ctx.send('Work in progress.')

    # Gundam

    @bot_commands.command()
    async def gundam(self, ctx):
        if allowed_channel(ctx):
            await ctx.trigger_typing()
            await ctx.send(file=discord.File(fp="images/gundam.png"))

    # Nimble
    @bot_commands.command()
    async def nimble(self, ctx):
        if allowed_channel(ctx):
            await ctx.trigger_typing()
            await ctx.send(file=discord.File(fp="images/nimble/horse" + str(random.randint(1, 20)) + ".jpg"))

    # Dad jokes
    @bot_commands.command()
    async def dad(self, ctx, *args):
        if allowed_channel(ctx):
            if len(args) > 0:
                await ctx.trigger_typing()
                await ctx.send("Hi, {}, I'm orb!".format(' '.join(args)))
            else:
                await ctx.trigger_typing()
                await ctx.send("Hi, *\"Person who doesn't know how to use this command\"*, I'm orb. Please enter at least one phrase to mock!")

    # Pablo
    @bot_commands.command()
    async def pablo(self, ctx, gauntlet=None):
        if allowed_channel(ctx):
            await ctx.trigger_typing()
            if (gauntlet == "gauntlet"):
                await ctx.send(file=discord.File(fp="images/pablo/infinity_final.png"))
                await ctx.send("> 5 OUT OF 5 OF THE INFINITY FLAMINGO GAUNTLET COSMETIC KIT HAS BEEN GATHERED")
            elif (gauntlet == "flamingo"):
                await ctx.send(file=discord.File(fp="images/pablo/pablo2.jpg"))
            else:
                if (random.randint(1, 10) >= 5):
                    await ctx.send(file=discord.File(fp="images/pablo/pablo2.jpg"))

    # Haze
    @bot_commands.command()
    async def haze(self, ctx):
        if allowed_channel(ctx):
            await ctx.trigger_typing()
            if random.randint(1, 10) > 8:
                await ctx.send("I want EVERY assignment done in:")
                await ctx.send("3")
                await asyncio.sleep(1)
                await ctx.send("2")
                await asyncio.sleep(1)
                await ctx.send("1")
                await asyncio.sleep(1)
                await ctx.send("Thanks for finishing those assignments! Remember: Liars get SMACK'd")
            else:
                await ctx.send(random.choice([("HAZE! ASSIGNMENTS! NOW!"), ("I swear on Sumako - if that assignment isn't done yet..."), ('"cranes are great" - Haze'), ("I don't want to hear you complaining about your assignments... EVER")]), )

    # Illya
    @bot_commands.command()
    async def illya(self, ctx):
        if allowed_channel(ctx):
            if random.randint(1, 50) == 2:
                await ctx.trigger_typing()
                await ctx.send(file=discord.File(fp="images/lolice.gif"))
            else:
                await ctx.trigger_typing()
                await ctx.send(file=discord.File(fp="images/illya/illya (" + str(random.randint(1, 47)) + ").jpg"))

    # Azsry
    @bot_commands.command()
    async def azsry(self, ctx):
        if not allowed_channel(ctx):
            return

        msgs = [
            """In C++ we don't say "Missing asterisk" we say ```error C2664: 'void std::vector<block,std::alocator<_Ty> >::push_back(const block &)': cannot convert argument 1 from 'std::_Vector_iterator<std::_Vector_val<std::_Simple_types<block> > >' to 'block &&'``` and i think that's beautiful""",
            "If A has friends then they can play with A's privates as well.",
            """```cpp
C++; // makes C bigger, returns old value```
            """,
            """"Knock Knock"
"Who's there?"
*very long pause*
"Java\""""
        ]

        await ctx.send(random.choice(msgs))

    # Gembutt
    @bot_commands.command()
    async def gembutt(self, ctx):
        if allowed_channel(ctx):
            await ctx.trigger_typing()
            await ctx.send(file=discord.File(fp="images/gembutt/gembutt (" + str(random.randint(1, 4)) + ").jpg"))

    # Kagepro
    @bot_commands.command()
    async def kagepro(self, ctx):
        if allowed_channel(ctx):
            await ctx.trigger_typing()
            await ctx.send(file=discord.File(fp="images/kagepro/kagepro (" + str(random.randint(1, 55)) + ").jpg"))

    # Yorimoi
    @bot_commands.command()
    async def yorimoi(self, ctx):
        if allowed_channel(ctx):
            await ctx.trigger_typing()
            await ctx.send(file=discord.File(fp="images/yorimoi/yorimoi (" + str(random.randint(1, 48)) + ").jpg"))

    # Fatepost
    @bot_commands.command()
    async def fatepost(self, ctx):
        if allowed_channel(ctx):
            await ctx.trigger_typing()
            await ctx.send(file=discord.File(fp="images/fate/fatepost (" + str(random.randint(1, 56)) + ").jpg"))

    # Rinpost
    @bot_commands.command()
    async def rinpost(self, ctx):
        if allowed_channel(ctx):
            await ctx.trigger_typing()
            await ctx.send(file=discord.File(fp="images/rinpost/rin (" + str(random.randint(1, 46)) + ").jpg"))

    # Touhou
    @bot_commands.command()
    async def touhou(self, ctx):
        if allowed_channel(ctx):
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
            if target is None:
                await ctx.send(":thinking:")
            else:
                for char in target.lower():
                    try:
                        output += TRANSLATE_DICT[char]
                    except:
                        output += char

                translation = discord.Embed(
                    description=str(output), colour=0xcb410b)
                translation.set_author(
                    name=ctx.author.display_name, icon_url=ctx.author.avatar_url)

                await ctx.send(embed=translation)

    # COVID info
    @bot_commands.command()
    async def covid(self, ctx):
        if not allowed_channel(ctx):
            return

        req = requests.get(
            "https://www.health.gov.au/news/health-alerts/novel-coronavirus-2019-ncov-health-alert")

        soup = BeautifulSoup(req.text, features="html.parser")
        alert_data = soup.find_all("ul", "field-health-alert-metadata__list")
        regex_results = re.findall("<\/small>(.*)?<\/li>", str(alert_data[0]))

        covid_alert_txt, last_update = regex_results
        covid_alert = regex_results[0] == "Active"

        req = requests.get(
            "https://www.qld.gov.au/health/conditions/health-alerts/coronavirus-covid-19/current-status/urgent-covid-19-update")
        soup = BeautifulSoup(req.text, features="html.parser")

        daily_cases = soup.select(".new > span")[0].decode_contents()
        total_cases = soup.select(".cases > span")[0].decode_contents()
        tests_conducted = soup.select(".tested > span")[0].decode_contents()
        total_vaccines = soup.select(".vaccine > span")[0].decode_contents()

        if len(soup.select(".alert-warning")) != 0:
            active_alerts = "\n\n----------------------\n\n"

        for x in soup.select(".alert-warning"):
            temp_soup = BeautifulSoup(str(x), features="html.parser")
            active_alerts += temp_soup.get_text().strip() + "\n\n"

        active_alerts += "----------------------\n\n"

        embed_data = {
            "title": f"COVID-19 information for {date.today()}",
            "type": "rich",
            "description": f"Alert: {covid_alert_txt} (Last updated {last_update}){active_alerts}Cases (last 24h): {daily_cases}\nTotal cases: {total_cases}\nTests conducted: {tests_conducted}\n Total vaccine doses: {total_vaccines}",
            "url": "https://www.covid19.qld.gov.au/",
            "color": 0xf55d42 if covid_alert else 0x11c255,
        }
        embed_obj = discord.Embed.from_dict(embed_data)
        embed_obj.set_image(
            url="https://www.qld.gov.au/__data/assets/image/0012/110460/Opengraph-default-thumbnail.png")

        await ctx.send(embed=embed_obj)


def setup(bot):
    bot.add_cog(CommandsCog(bot))
