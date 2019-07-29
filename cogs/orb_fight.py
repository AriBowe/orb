import discord
from discord.ext import commands as bot_commands
import random
import csv
import re

from cogs.orb_control import allowed_channel

class FightCog(bot_commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("orb_fight loaded")

    # Fight someone
    @bot_commands.command()
    async def fight(self, ctx, target=None):
        if allowed_channel(ctx):
            if target is None:
                await ctx.send("You can't fight nothing")
            elif str(target)[0:2] != "<@":
                await ctx.send("Please tag a user to fight them")
            else:
                print(ctx.author.display_name + " is fighting " + target)

            if str("<@" + ctx.author.id + ">") == target:
                await ctx.send(ctx.author.display_name + "hurt themselves in their confusion!")
            else:
                caller = str("<@" + ctx.author.id + ">")
                caller_found = False
                caller_str = 0
                caller_def = 0
                caller_spd = 0

                target_found = False
                target_str = 0
                target_def = 0
                target_spd = 0

                with open("data/fight.csv", mode="r", newline="") as file:
                    reader = csv.reader(file, delimiter=",")
                    for line in reader:
                        try:       
                            if line[0] == caller:
                                caller_found = True
                                caller_str = line[1]
                                caller_def = line[2]
                                caller_spd = line[3]
                                return
                        except:
                            caller_found = False
                    for line in reader:
                        try:       
                            if line[0] == target:
                                target_found = True
                                target_str = line[1]
                                target_def = line[2]
                                target_spd = line[3]
                                return
                        except:
                            target_found = False
                
                if caller_found is False:
                    with open("data/fight.csv", mode="a", newline="") as file:
                        caller_str = random.randint(1,10)
                        caller_def = random.randint(1,10)
                        caller_spd = random.randint(1,10)

                        writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)    
                        writer.writerow([caller, caller_str, caller_def, caller_spd])

                if target_found is False:
                    with open("data/fight.csv", mode="a", newline="") as file:
                        target_str = random.randint(1,10)
                        target_def = random.randint(1,10)
                        target_spd = random.randint(1,10)

                        writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)    
                        writer.writerow([target, target_str, target_def, target_spd])

                caller_luck = random.randint(-2, 2)
                target_luck = random.randint(-2, 2)

                caller_health = 5
                target_health = 5

                caller_name = ctx.author.display_name
                target_name = get_member(target[2:-1])

                if caller_spd + caller_luck + 3 >= target_spd + target_luck:
                    #fight
                    pass
                elif caller_spd + caller_luck + 5 >= target_spd + target_luck:
                    await ctx.send(random.choice([str(caller_name + " tried to start a fight with " + target_name + ", but they barely escaped"), str(caller_name + " tried to start a fight with " + target_name + ", but managed to slip away"),]))
                else:
                    await ctx.send(random.choice([str(caller_name + " tried to start a fight with " + target_name + ", but they couldn't catch them"), str(caller_name + " couldn't catch " + target_name)]))

def setup(bot):
    bot.add_cog(FightCog(bot))