import discord
from discord.ext import commands as bot_commands
import random
import csv
import re
import asyncio

from cogs.orb_control import allowed_channel

class FightCog(bot_commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        print("orb_fight loaded")

    # Fight someone
    # TODO: Split this up, it's massive
    @bot_commands.command()
    async def fight(self, ctx, target=None):
        async def generate_new_user(self, user_id):
            numbers = sorted(random.sample(range(1, 10), 2))
            _str = numbers[0]
            _def = numbers[1] - numbers[0]
            _spd = 15 - numbers[1]

            with open("data/fight.csv", mode="a", newline="") as file:
                writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)    
                writer.writerow([user_id, _str, _def, _spd])

        if allowed_channel(ctx):
            if target is None:
                await ctx.send("You can't fight nothing")
                return None
            elif len(ctx.message.mentions) != 1:
                await ctx.send("Please tag a user to fight them")
                return None
            else:
                print(ctx.author.display_name + " is fighting " + target)

            target = ctx.message.mentions[0]
            caller = ctx.author

            if caller == target:
                await ctx.send(random.choice([str(str(ctx.author.display_name) + " hurt themselves in their confusion!"), "You punch youself in the face", "You high-five a brick wall with your head", "You try to drop-kick yourself and fall over"]))
            else:
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
                            if line[0] == str(caller.id):
                                caller_found = True
                                caller_str = int(line[1])
                                caller_def = int(line[2])
                                caller_spd = int(line[3])
                                break
                        except:
                            caller_found = False
                    for line in reader:
                        try:       
                            if line[0] == str(target.id):
                                target_found = True
                                target_str = int(line[1])
                                target_def = int(line[2])
                                target_spd = int(line[3])
                                break
                        except:
                            target_found = False
                
                if caller_found is False:
                    await generate_new_user(self, caller.id)

                if target_found is False:
                    await generate_new_user(self, target.id)

                caller_luck = random.randint(-1, 1)
                target_luck = random.randint(-1, 1)

                caller_health = 3
                target_health = 3
                caller_grappled = False
                target_grappled = False

                caller_name = caller.display_name
                target_name = target.display_name

                # print("---")
                # print("Caller")
                # print("id: " + caller)
                # print("name: " + caller_name)
                # print("found: " + str(caller_found))
                # print("str: " + str(caller_str))
                # print("def: " + str(caller_def))
                # print("spd: " + str(caller_spd))
                # print("luck: " + str(caller_luck))
                # print("health: " + str(caller_health))
                # print("---")
                # print("Target")
                # print("id: " + target)
                # print("name: " + target_name)
                # print("found: " + str(target_found))
                # print("str: " + str(target_str))
                # print("def: " + str(target_def))
                # print("spd: " + str(target_spd))
                # print("luck: " + str(target_luck))
                # print("health: " + str(target_health))
                # print("---")

                if caller_spd + caller_luck + 3 >= target_spd + target_luck or random.random() < 0.8:
                    await ctx.send("**" + random.choice([str(caller_name + " started a fight with " + target_name), str(caller_name + " is fighting " + target_name), str(caller_name + " and " + target_name + " are fighting!")]) + "**")
                elif caller_spd + caller_luck + 5 >= target_spd + target_luck or random.random() < 0.6:
                    await ctx.send(random.choice([str(caller_name + " tried to start a fight with " + target_name + ", but they barely escaped"), str(caller_name + " tried to start a fight with " + target_name + ", but managed to slip away"),]))
                    return
                else:
                    await ctx.send(random.choice([str(caller_name + " tried to start a fight with " + target_name + ", but they couldn't catch them"), str(caller_name + " couldn't catch " + target_name)]))  
                    return

                while target_health >= 0 or caller_health >= 0:
                    if caller_grappled:
                        # Try and recover
                        
                        if random.random() + (caller_luck / 10) > 0.5:
                            caller_grappled = False
                            # Caller free
                            await ctx.send(random.choice([
                                (caller_name + " manages to get back on their feet"),
                                (caller_name + " gets out of the grapple")
                            ]))

                        else:
                            # Caller still grappled   
                            await ctx.send(random.choice([
                                (caller_name + " can't get up"),
                                (caller_name + " fails to escape the grapple")
                            ]))

                    if target_grappled and not caller_grappled:
                        # Attack grappled target
                        if caller_str > target_def:
                            target_health -= 2
                            # Major attack
                            await ctx.send(random.choice([
                                (caller_name + " gets a good hit on " + target_name),
                                (target_name + " is kicked while they're down"),
                            ]))

                        elif caller_str > target_def - 3:
                            target_health -= 1
                            # Minor attack
                            await ctx.send(random.choice([
                                (caller_name + " lands a blow on the grappled " + target_name),
                                (caller_name + " gets some hits in while " + target_name + "  is down"),
                            ]))


                    # Caller attacks first
                    elif random.random() > 0.9 and not caller_grappled:
                        target_health -= 2
                        # Major attack
                        await ctx.send(random.choice([
                                (caller_name + " kicks " + target_name + " hard"),
                                (target_name + " takes a punch square in the face"),
                                (target_name + " is hit hard a couple of times by " + caller_name)
                            ]))

                    elif random.random() > 0.8 and not caller_grappled:
                        stat = random.randint(1, 3)
                        if stat == 0:
                            target_health -= 1
                            target_str -= random.randint(1,2)
                            # Str damage
                            await ctx.send(random.choice([
                                (caller_name + " gets " + target_name + " in the stomach, winding them"),
                                (target_name + " gets bruised up, and can't move as well"),
                                (target_name + " has the wind knocked out of them by " + caller_name)
                            ]))

                        elif stat == 1:
                            target_spd -= random.randint(1,2)
                            # Spd damage
                            await ctx.send(random.choice([
                                (caller_name + " hurts " + target_name + "'s legs"),
                                (target_name + " think's they've sprained something"),
                            ]))

                        else:
                            target_def -= random.randint(1,2)
                            # Def damage
                            await ctx.send(random.choice([
                                (caller_name + " dazes " + target_name),
                                (target_name + " can't see too well"),
                                (target_name + " feels dizzy")
                            ]))

                    elif random.random() > 0.6 and not caller_grappled:
                        # Target catches attack
                        if target_def + target_luck + random.randint(-2,2) > caller_str + caller_luck + 3:
                            caller_health -= 1
                            # Lucky hit by target
                            await ctx.send(random.choice([
                                (target_name + " gets a lucky shot in"),
                                (target_name + " is attacked by " + caller_name + ", but they fight them off")
                            ]))

                        elif target_def + target_luck + random.randint(-2,2) > caller_str + caller_luck:
                            # Target blocks 
                            await ctx.send(random.choice([
                                (caller_name + " kicks at " + target_name + " , but they dodge"),
                                (target_name + " manages to block most of " + caller_name + "'s punches"),
                                (target_name + " isn't fazed by " + caller_name + "'s attacks")]))

                        elif target_def + target_luck + random.randint(-2,2) > caller_str + caller_luck -3:
                            target_health -= 1
                            # Standard damage
                            await ctx.send(random.choice([
                                (caller_name + " hits " + target_name + " in the ribs"),
                                (target_name + " takes a punch or two"),
                                (target_name + " is hurt by " + caller_name),
                                (caller_name + " lands a blow")
                            ]))
                            
                        else:
                            target_health -= 2
                            # Major damage
                            await ctx.send(random.choice([
                                (caller_name + " gets through " + target_name + "'s defences and hits hard"),
                                (target_name + " can't dodge " + caller_name + "'s attacks"),
                            ]))

                    elif random.random() > 0.75 and not caller_grappled:
                        # Attempt a grapple
                        if target_spd + target_luck + random.randint(-2,2) < caller_spd + caller_luck + random.randint(-2,2) and target_grappled is False and caller_grappled is False:
                            target_grappled = True
                            caller_grappled = True
                            # Grapple passes
                            await ctx.send(random.choice([
                                (caller_name + " grabs on to " + target_name + " and holds tight"),
                                (target_name + " and " + caller_name + " get pulled to the ground"),
                                (target_name + " gets jumped on by " + caller_name)
                            ]))

                        elif target_spd + target_luck + random.randint(-2,2) > caller_spd + caller_luck + random.randint(-2,2) + 1 and target_grappled is False and caller_grappled is False:
                            target_grappled = True
                            caller_grappled = True
                            caller_health -= 1
                            # Grapple passes but with damage
                            await ctx.send(random.choice([
                                (caller_name + " trips " + target_name + " and they both fall"),
                                (target_name + " is knocked over, but pulls " + caller_name + " down with them")
                            ]))

                        else:
                            # Grapple fails
                            await ctx.send(random.choice([
                                (caller_name + " tries to grab " + target_name + " but fails"),
                                (target_name + " stumbles but doesn't fall")
                            ]))

                    elif not caller_grappled:
                        # Failed attack from caller
                        await ctx.send(random.choice([
                                (caller_name + " tries to hit " + target_name + " but can't land a blow"),
                                (target_name + " dodges " + caller_name + "'s attacks"),
                                (target_name + " holds off " + caller_name)
                            ]))
                    
                    else:
                        pass

                    if target_health <= 0 or caller_health <= 0:
                        break
                    
                    # Target's turn
                    if target_grappled:
                       # Try and recover
                      
                        if random.random() + (target_luck / 10) > 0.5:
                            target_grappled = False
                            # target free
                            await ctx.send(random.choice([
                                (target_name + " manages to get back on their feet"),
                                (target_name + " gets out of the grapple")
                            ]))
    
                        else:
                            # target still grappled  
                            await ctx.send(random.choice([
                                (target_name + " can't get up"),
                                (target_name + " fails to escape the grapple")
                            ]))
 
                    if caller_grappled and not target_grappled:
                        # Attack grappled caller
                        if target_str > caller_def:
                            caller_health -= 2
                            # Major attack
                            await ctx.send(random.choice([
                                (target_name + " gets a good hit on " + caller_name),
                                (caller_name + " is kicked while they're down"),
                            ]))
    
                        elif target_str > caller_def - 3:
                            caller_health -= 1
                            # Minor attack
                            await ctx.send(random.choice([
                                (target_name + " lands a blow on the grappled " + caller_name),
                                (target_name + " gets some hits in while " + caller_name + "is down"),
                            ]))
    
    
                    # target attacks first
                    elif random.random() > 0.9 and not target_grappled:
                        caller_health -= 2
                        # Major attack
                        await ctx.send(random.choice([
                                (target_name + " kicks " + caller_name + " hard"),
                                (caller_name + " takes a punch square in the face"),
                                (caller_name + " is hit hard a couple of times by " + target_name)
                            ]))
    
                    elif random.random() > 0.8 and not target_grappled:
                        stat = random.randint(1, 3)
                        if stat == 0:
                            caller_health -= 1
                            caller_str -= random.randint(1,2)
                            # Str damage
                            await ctx.send(random.choice([
                                (target_name + " gets " + caller_name + " in the stomach, winding them"),
                                (caller_name + " gets bruised up, and can't move as well"),
                                (caller_name + " has the wind knocked out of them by " + target_name)
                            ]))
    
                        elif stat == 1:
                            caller_spd -= random.randint(1,2)
                            # Spd damage
                            await ctx.send(random.choice([
                                (target_name + " hurts " + caller_name + "'s legs"),
                                (caller_name + " think's they've sprained something"),
                            ]))
    
                        else:
                            caller_def -= random.randint(1,2)
                            # Def damage
                            await ctx.send(random.choice([
                                (target_name + " dazes " + caller_name),
                                (caller_name + " can't see too well"),
                                (caller_name + " feels dizzy")
                            ]))
    
                    elif random.random() > 0.6 and not target_grappled:
                        # caller catches attack
                        if caller_def + caller_luck + random.randint(-2,2) > target_str + target_luck + 3:
                            target_health -= 1
                            # Lucky hit by caller
                            await ctx.send(random.choice([
                                (caller_name + " gets a lucky shot in"),
                                (caller_name + " is attacked by " + target_name + ", but they fight them off")
                            ]))
    
                        elif caller_def + caller_luck + random.randint(-2,2) > target_str + target_luck:
                            # caller blocks
                            await ctx.send(random.choice([
                                (target_name + " kicks at " + caller_name + " , but they dodge"),
                                (caller_name + " manages to block most of " + target_name + "'s punches"),
                                (caller_name + " isn't fazed by " + target_name + "'s attacks ")
                            ]))
    
                        elif caller_def + caller_luck + random.randint(-2,2) > target_str + target_luck -3:
                            caller_health -= 1
                            # Standard damage
                            await ctx.send(random.choice([
                                (target_name + " hits " + caller_name + " in the ribs"),
                                (caller_name + " takes a punch or two"),
                                (caller_name + " is hurt by " + target_name),
                                (target_name + " lands a blow")
                            ]))
                            
                        else:
                            caller_health -= 2
                            # Major damage
                            await ctx.send(random.choice([
                                (target_name + " gets through " + caller_name + "'s defences and hits hard"),
                                (caller_name + " can't dodge " + target_name + "'s attacks"),
                            ]))
    
                    elif random.random() > 0.75 and not target_grappled:
                        # Attempt a grapple
                        if caller_spd + caller_luck + random.randint(-2,2) < target_spd + target_luck + random.randint(-2,2) and caller_grappled is False and target_grappled is False:
                            caller_grappled = True
                            target_grappled = True
                            # Grapple passes
                            await ctx.send(random.choice([
                                (target_name + " grabs on to " + caller_name + " and holds tight"),
                                (caller_name + " and " + target_name + " get pulled to the ground"),
                                (caller_name + " gets jumped on by " + target_name)
                            ]))
    
                        elif caller_spd + caller_luck + random.randint(-2,2) > target_spd + target_luck + random.randint(-2,2) + 1 and caller_grappled is False and target_grappled is False:
                            caller_grappled = True
                            target_grappled = True
                            target_health -= 1
                            # Grapple passes but with damage
                            await ctx.send(random.choice([
                                (target_name + " trips " + caller_name + " and they both fall"),
                                (caller_name + " is knocked over, but pulls " + target_name + " down with them")
                            ]))
    
                        else:
                            # Grapple fails
                            await ctx.send(random.choice([
                                (target_name + " tries to grab " + caller_name + " but fails"),
                                (caller_name + " stumbles but doesn't fall")
                            ]))
    
                    elif not target_grappled:
                        # Failed attack from target
                        await ctx.send(random.choice([
                                (target_name + " tries to hit " + caller_name + " but can't land a blow"),
                                (caller_name + " dodges " + target_name + "'s attacks"),
                                (caller_name + " holds off " + target_name)
                            ]))
                    
                    else:
                        pass
                    await ctx.trigger_typing()
                    await asyncio.sleep(4)
                    # await ctx.send(str(target_health) + " T | C " + str(caller_health))

                if target_health > caller_health:
                    winner = target_name
                    loser = caller_name
                elif target_health < caller_health:
                    winner = caller_name
                    loser = target_name
                else:
                    await ctx.send("Both fighters faint")
                    return

                await ctx.send(random.choice([
                                (winner + " is victorious"),
                                (winner + " has won this battle"),
                                (winner + " defeats " + loser),
                                (loser + " is knocked out"),
                                (winner + " floors " + loser)
                            ]))

    # Fighter stats
    @bot_commands.command(aliases=["fight_stats"])      
    async def stats(self, ctx, target=None):
        if allowed_channel(ctx):
            if target is None:
                await ctx.send("Please tag something")
                return None
            elif len(ctx.message.mentions) != 1:
                await ctx.send("Please tag one user")
                return None

            target = ctx.message.mentions[0]
            found = False

            with open("data/fight.csv", mode="r", newline="") as file:
                reader = csv.reader(file, delimiter=",")
                for line in reader:
                    try:       
                        if line[0] == str(target.id):
                            found = True
                            _str = int(line[1])
                            _def = int(line[2])
                            _spd = int(line[3])
                            break
                    except:
                       found = False
            
            if found:
                embed = discord.Embed(title="Fighter Stats", colour=0xcb410b)
                embed.set_author(name=target.display_name, icon_url=target.avatar_url)
                embed.add_field(name="STR", value=_str, inline=True)
                embed.add_field(name="DEF", value=_def, inline=True)
                embed.add_field(name="SPD", value=_spd, inline=True)

                await ctx.send(embed=embed)

            else:
                embed = discord.Embed(title="Fighter Stats", description="This user has not generated any stats. Fight them to make some!", colour=0xcb410b)
                embed.set_author(name=target.display_name, icon_url=target.avatar_url)

                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(FightCog(bot))