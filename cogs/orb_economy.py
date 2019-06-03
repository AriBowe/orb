import discord
from discord.ext import commands as bot_commands
import csv
import random

class UserManagement():
    """General management for orb users"""
    def __init__(self):
        """Constructor"""
        self._active_users = []
    
    def save(self):
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
    
    async def add_active(self, user):
        self._active_users.append(user)
    

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

class Orb():
    """Representation of an orb, the basic unit of an item.
    Should not be initialised on its own"""
    def __init__(self):
        pass
    
    async def get_type(self):
        pass

    async def get_integrity(self):
        pass

    async def get_rarity(self):
        pass