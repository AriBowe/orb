import discord
import requests
import asyncio
import os
from discord.utils import get
from discord.ext import commands as bot_commands
from discord.ext import tasks
from discord import DMChannel

client = discord.Client()

FOLLOWERS = 'data/followers.txt'
URL = 'https://api.github.com/repos/AriBowe/orb/pulls'

myobj = {'somekey': 'somevalue'}
info = ['title', 'body', 'html_url', 'id', 'created_at']

'''
Get all information from the github api about any new pull requests in orb
'''


async def get_response(request, data):
    full = requests.get(request, data)
    return list(full.json())

'''
Finds all relevant information about the user who made the request
'''


async def find_user_info(resp):
    user = {}
    full = resp['user']
    # find all important information and store it respectively
    user['name'] = full['login']
    user['profile'] = full['html_url']
    user['type'] = full['type']
    user['avatar'] = full['avatar_url']
    user['id'] = full['id']
    return user

'''
Populates the pr dictionary with all relevant information
'''


async def populate_prs(resp):
    pull_requests = {}
    for pull in resp:
        all_info = {}
        piece = dict(pull)

        all_info['USER'] = await find_user_info(pull)
        for title in info:
            all_info[title.upper()] = str(pull[title])

        pull_requests[all_info['ID']] = all_info

    return pull_requests

'''
create one embed to format up
'''


async def format_embed(pull):
    # check if a description to the commit exists
    footer = False
    if (len(pull['BODY']) < 1):
        pull['BODY'] = '''A new pull request was posted at 
        approximately ''' + pull['CREATED_AT']
        footer = True

    # setup initial embed
    embed = discord.Embed(title=pull['TITLE'],
                          url=pull['HTML_URL'],
                          description=pull['BODY'],
                          color=0xFF5733)

    # get the author going
    embed.set_author(name=pull['USER']['name'],
                     url=pull['USER']['profile'],
                     icon_url=pull['USER']['avatar'])

    # Create a footer with the time of the pull request
    embed.set_footer(text='''This pull request was posted at 
    approximately ''' + pull['CREATED_AT'])

    return embed

'''
format all embeds up
'''


async def format_all_embeds(pullRequests):
    all_embeds = []
    for pull in pullRequests.values():
        all_embeds.append(await format_embed(pull))
    return all_embeds


class PullsCog(bot_commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.embed()

    '''
    Return a user object given the user ID
    '''
    async def find_user(self, userId):
        return await self.bot.fetch_user("{}".format(userId))

    '''
    Get all user objects that need to be informated
    '''
    async def find_all_users(self, directory):
        users = []
        followers = open(directory, 'r')
        lines = followers.readlines()
        # iterate through all lines finding all the user IDs
        for line in lines:
            # add the respective user obejcts to our list
            if (len(line.strip()) > 0):
                users.append(await self.find_user(line))
        followers.close()
        return users

    @bot_commands.Cog.listener()
    async def on_ready(self):
        await self.embed.start()

    @tasks.loop(hours=3)  # every 3 hours at the moment
    async def embed(self):
        channel = self.bot.get_channel(823075283942375458)
        users = await self.find_all_users(FOLLOWERS)

        # make the request and format all related embeds respective of response
        resp = await get_response(URL, data=myobj)

        pullRequests = await populate_prs(resp)
        all_embeds = await format_all_embeds(pullRequests)

        # send the pull request to all followers
        for embed in all_embeds:
            for user in users:
                await DMChannel.send(user, embed=embed)


def setup(bot):
    bot.add_cog(PullsCog(bot))
