import discord
from discord.ext import commands as bot_commands
import csv

BANNED_CHANNELS = []

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


class ControlCog(bot_commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    # Manual speaking
    @bot_commands.command()
    async def say(self, ctx, channel, *, target=None):
        if ctx.author.id == 138198892968804352:
            if target == None:
                await ctx.send("Need a message")
            else:
                channel = self.bot.get_channel(int(channel))
                print("Sent message", str(target), "to channel", str(channel))
                await channel.send(target)

    # Update banned channels
    @bot_commands.command()
    async def update_banned(self, ctx):
        if ctx.author.id == 138198892968804352:
            BANNED_CHANNELS = []
            with open("data/banned_channels.csv", mode="r", newline="") as file:
                reader = csv.reader(file, delimiter=",")
                for line in reader:
                    try:
                        BANNED_CHANNELS.append(int(line[0]))
                    except:
                        pass
            await ctx.send("Done!")

    # Add a new banned channel
    @bot_commands.command()
    async def add_banned(self, ctx, target, *, comment=None):
        if ctx.author.id == 138198892968804352:
            print("Adding", target, "to banned channels list with comment", comment)
            with open("data/banned_channels.csv", mode="a", newline="") as file:
                writer = csv.writer(file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)
                writer.writerow([target, str(" # " + comment)])
            await ctx.send("Done!")

    # Remove a banned channel
    @bot_commands.command()
    async def remove_banned(self, ctx, target):
        if ctx.author.id == 138198892968804352:
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
                    if line[0] != target:
                        writer.writerow(line)
            temp=[]
            await ctx.send("Done!")

    # Lists banned channels
    @bot_commands.command()
    async def list_banned(self, ctx):
        if ctx.author.id == 138198892968804352:
            output = ""
            with open("data/banned_channels.csv", mode="r", newline="") as file:
                for line in file:
                    output += "Channel: " + line + "\n"
                await ctx.send(output)

def setup(bot):
    bot.add_cog(ControlCog(bot))