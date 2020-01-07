"""
Handles general control tasks and acts as a function generaliser for other commands. Also contains some admin-only commands and runs the database
"""

import discord
from discord.ext import commands as bot_commands
import csv
import os
from google.cloud import firestore

from utils.repo import ADMINS

# Verifies if the command is allowed to be executed
# This is a utility function and shouldn't be called on it's own (hence the lack of .command decorator)
# Not async because a). Incredibly low complexity (aka fast)
#                   b). This is a priority to execute
#                   c). Nothing would be awaited in here so an async function would work the same as a regular
def allowed_channel(ctx):
    if ctx in BANNED_CHANNELS:
        return False
    else:
        return True

# Connects to Cloud Firestore
print("Verifiying with server")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="firestore_key.json"
db = firestore.Client()
print("Connected to Google Cloud Firestore")

BANNED_CHANNELS = db.collection("banned_channels").stream()     # This needs to be here just trust me -Ari


class ControlCog(bot_commands.Cog):
    def __init__(self, bot):
        self.bot = bot
#         print("orb_control loaded")
        
    # Manual speaking
    @bot_commands.command()
    async def say(self, ctx, channel, *, target=None):
        if ctx.author.id in ADMINS:
            if target == None:
                await ctx.send("Need a message")
            else:
                channel = self.bot.get_channel(int(channel))
                print("Sent message", str(target), "to channel", str(channel))
                await channel.send(target)

    # Update banned channels
    @bot_commands.command()
    async def update_banned(self, ctx):
        if ctx.author.id in ADMINS:
            BANNED_CHANNELS = []
            with open("data/banned_channels.csv", mode="r", newline="") as file:
                reader = csv.reader(file, delimiter=",")
                for line in reader:
                    BANNED_CHANNELS.append(int(line[0]))
                    print(BANNED_CHANNELS)
            await ctx.send("Done!")

    # Add a new banned channel
    @bot_commands.command()
    async def add_banned(self, ctx, target, *, comment=None):
        if ctx.author.id in ADMINS:
            print("Adding", target, "to banned channels list with comment", comment)
            with open("data/banned_channels.csv", mode="a", newline="") as file:
                writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([target, str(" # " + str(comment))])
            await ctx.send("Done!")

    # Remove a banned channel
    @bot_commands.command()
    async def remove_banned(self, ctx, target):
        if ctx.author.id in ADMINS:
            print("Removing", target, "from banned channels list")
            print(type(target))
            temp = []
            with open("data/banned_channels.csv", mode="r", newline="") as file:
                try:
                    temp = list(csv.reader(file, delimiter=","))
                except:
                    pass
            with open("data/banned_channels.csv", mode="w", newline="") as file:
                writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for line in temp:
                    try:
                        if line[0] != target:
                            try:
                                writer.writerow(line)
                            except:
                                pass
                    except:
                        pass
            temp=[]
            await ctx.send("Done!")

    # Lists banned channels
    @bot_commands.command()
    async def list_banned(self, ctx):
        if ctx.author.id in ADMINS:
            output = ""
            with open("data/banned_channels.csv", mode="r", newline="") as file:
                for line in file:
                    output += "Channel: " + line + "\n"
                await ctx.send(output)

def setup(bot):
    bot.add_cog(ControlCog(bot))
