import discord
from discord.ext import commands as bot_commands
import csv
import random
import asyncio
import datetime

client = discord.Client()

class UserManagement():
    """General management for orb users"""
    def __init__(self):
        """Constructor"""
        self._active_users = []
        self._autosave = False
    
    async def save(self):
        """Saves the users
        
        A bit of a mess of a function, but it basically does 3 major tasks
            1). Loads the data of all the users who aren't in the active
                users list into a list of all users
            2). Gets the saveable data representation of all the active
                users and appends them onto the end of the list
            3). Clears the file containing all of the users and writes the
                all users list over it, then blanks the all users list
                
        I realise how dangerous this is, but CSV doesn't allow you to change
        data on a line without doing this. This should get shifted to a SQL
        database eventually"""

        with open("data/orbs.csv", mode="r", newline="") as file:
            all_users_list = []
            reader = csv.reader(file, delimiter=";")
            for line in reader:
                if line[0] not in self._active_users:
                    all_users_list.append(list(line))
            print(all_users_list)
        
        for user in self._active_users:
            all_users_list.append(user.generate_line())

        with open("data/orbs.csv", mode="w", newline="") as file:
            writer = csv.writer(file, delimiter=";", quotechar='"', quoting=csv.QUOTE_MINIMAL)
            for user in all_users_list:
                writer.writerow(user)

        self._active_users = []

    async def save_loop(self):
        """Automatic saving loop, designed to save every minute rather than on a trigger"""
        while self._autosave:
            self.save()
            asyncio.sleep(60)

    async def add_active(self, user_id):
        self._active_users.append(User(user_id))

    async def check_active(self, user_id):
        if user_id in self._active_users:
            return True
        else:
            return False

    def break_next_save(self):
        self._autosave = False
    

class User():
    """An orb user, this class manages their economy"""
    def __init__(self, user_id):
        """Constructor
        
        NOTE: This probably should be an SQL database but I can't be
        fucked learning SQL for this update. I'll probably update it once
        I can be bothered or if it becomes a problem. The messy dictionary
        setup is because users can have an arbitrary number of unique orb
        types.

        Parameters:
            user_id (str): The discord user ID of the target to load"""
        with open("data/orbs.csv", mode="r", newline="") as file:
            reader = csv.reader(file, delimiter=";")
            for line in reader:
                try:
                    if line[0] == str(user_id):
                        user_id = line[0]
                        user_status = line[1]
                        user_shards = line[2]

                        orb_data = line[3:]
                        tupify = lambda x : x.split(",")
                        user_orbs = dict(map(tupify, orb_data))
                except:
                    pass
        
        for orb_type in user_orbs:
            user_orbs[orb_type] = int(user_orbs[orb_type])

        self.user_id = user_id
        self._user_status = user_status
        self._user_shards = user_shards
        self._user_orbs = user_orbs

    async def get_orbs(self, orb_type):
        try:
            return self._user_orbs[orb_type]
        except:
            return None
            

    async def add_orbs(self, orb_type, orb_count):
        if orb_type in self._user_orbs:
            self._user_orbs[orb_type] += orb_count
        else:
            self._user_orbs[orb_type] = orb_count

    async def remove_orbs(self, orb_type, orb_count):
        if orb_type in self._user_orbs:
            self._user_orbs[orb_type] -= orb_count
            if self._user_orbs[orb_type] <= 0:
                self._user_orbs.pop(orb_type)
        else:
            pass

    async def get_shards(self):
        return self._user_shards

    async def add_shards(self, shard_count):
        self._user_shards += shard_count

    async def remove_shards(self, shard_count):
        self._user_shards -= shard_count

    async def get_status(self):
        return self._user_status

    async def generate_line(self):
        # flattened_dict = ';'.join('"{!s}",{!r}'.format(item,self._user_orbs[item]) for item in self._user_orbs)

        output = []
        output.append(self.user_id)
        output.append(self.get_status())
        output.append(self.get_shards())
        for item in self._user_orbs:
	        output.append('"{!s}",{!r}'.format(item,self._user_orbs[item]))

        return output



rarity_table = {
    0: "common",
    1: "uncommon",
    2: "rare",
    3: "mythical",
    4: "unique"
}

class Orb():
    """Representation of an orb, the basic unit of an item.
    Should not be initialised on its own"""
    def __init__(self):
        pass
    
    async def get_type(self):
        """The orb type, aka the name"""
        raise NotImplementedError

    async def get_integrity(self):
        """How many times the orb can be used before breaking"""
        return 1

    async def get_rarity(self):
        """How rare the orb is, following rarity_table"""
        return 0

# --- All the orbs ---

class ChaoticOrb(Orb):
    """Randomises a stat"""
    
    async def get_type(self):
        return "Chaotic"

    async def get_rarity(self):
        return 1

class EnergyOrb(Orb):
    """Changes a bde stat by a small amount"""

    async def get_type(self):
        return "Energy"

class RankOrb(Orb):
    """Changes a rank stat by a small amount"""

    async def get_type(self):
        return "Rank"

class TransmutationOrb(Orb):
    """Transmutes another orb to the same rarity or lower"""

    async def get_type(self):
        return "Transmutation"

    async def get_integrity(self):
        return 3

    async def get_rarity(self):
        return 2

class ImmuneOrb(Orb):
    """Makes a user immune to orb reacts, rank, and BDE for a limited time"""

    async def get_type(self):
        return "Immunity"

    async def get_rarity(self):
        return 1

# --- Economy interaction cog ---

class EconomyCog(bot_commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._users = UserManagement()

        print("orb_economy loaded")

    @bot_commands.command()
    async def economy(self, ctx):
        self._author = ctx.author
        
        def check(reaction, user):
            print("Checking")
            return user == self._author and (str(reaction.emoji) == '🗃' or str(reaction.emoji) == '🗓' or str(reaction.emoji) == '✉' or str(reaction.emoji) == '⚙')

        main_embed=discord.Embed(title="\u200b", desciption="Click on one of the reactions below to select that option", color=0xcb410b)
        main_embed.set_author(name="ORB ECONOMY", icon_url="https://cdn.discordapp.com/avatars/569758271930368010/3b243502ea9079f6a4f33fb0e270105c.webp?size=1024")
        main_embed.add_field(name="🗃️ Inventory", value="\u200b", inline=False)
        main_embed.add_field(name="🗓️ Daily", value="\u200b", inline=False)
        main_embed.add_field(name="✉️ Send Orbs/Shards", value="\u200b", inline=False)
        main_embed.add_field(name="⚙️ Use Orbs/Shards", value="\u200b", inline=False)
        main_embed.set_footer(text="This window will time out after 45 seconds of inactivity")
        
        timeout_embed=discord.Embed(title=" ", color=0xcb410b)
        timeout_embed.set_author(name="ORB ECONOMY", icon_url="https://cdn.discordapp.com/avatars/569758271930368010/3b243502ea9079f6a4f33fb0e270105c.webp?size=1024")
        timeout_embed.add_field(name="Error: Timed out", value="Responses must be within 45 seconds", inline=False)

        message = await ctx.send(embed=main_embed)
        await message.add_reaction("🗃")
        await message.add_reaction("🗓")
        await message.add_reaction("✉")
        await message.add_reaction("⚙")

        try:
            reaction, user = await self.bot.wait_for('reaction_add', timeout=45.0, check=check)
        except asyncio.TimeoutError:
            await message.edit(embed=timeout_embed)
            await ctx.remove_reaction(reaction.emoji, user)

        else:
            if reaction.emoji == "🗃":
                pass
            elif reaction.emoji == "🗓":
                pass
            elif reaction.emoji == "✉":
                pass
            elif reaction.emoji == "✉":
                pass
            else:
                pass


def setup(bot):
    bot.add_cog(EconomyCog(bot))