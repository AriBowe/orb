import discord
import time
import os
import psutil
import datetime

from datetime import datetime
from discord.ext import commands
from utils import default, repo


class Information(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())
        if not hasattr(self.bot, 'uptime'):
            self.bot.uptime = datetime.datetime.now()

    @commands.command()
    async def ping(self, ctx):
        """Measures ping"""
        before = time.monotonic()
        message = await ctx.send('Pong!')
        ping = (time.monotonic() - before)
        await message.edit(content=f'Pong! | `{int(ping) * 1000} ms`')

    @commands.command(aliases=['botinfo', 'botstats', 'botstatus'])
    async def aboutbot(self, ctx):
        """ About the bot """
        ram_usage = self.process.memory_full_info().rss / 1024**2
        avg_members = round(len(self.bot.users) / len(self.bot.guilds))

        embed = discord.Embed(colour=ctx.me.top_role.colour)
        embed.set_thumbnail(url=ctx.bot.user.avatar_url)
        embed.add_field(name="Last boot", value=default.timeago(datetime.now() - self.bot.uptime), inline=True)
        embed.add_field(
            name=f"Developer: Ari Bowe",
            # value=', '.join([str(self.bot.get_user(x)) for x in self.config.owners]),
            inline=True)
        embed.add_field(name="Library", value="discord.py", inline=True)
        embed.add_field(name="Servers", value=f"{len(ctx.bot.guilds)} ( avg: {avg_members} users/server )", inline=True)
        embed.add_field(name="Commands loaded", value=str(len([x.name for x in self.bot.commands])), inline=True)
        embed.add_field(name="RAM", value=f"{ram_usage:.2f} MB", inline=True)

        await ctx.send(content=f"ℹ About **{ctx.bot.user}** | **{repo.VERSION_DATA['Version']}**", embed=embed)

    @commands.command()
    async def about(self, ctx, member: discord.Member = None):
        """About a member"""
        if member is None:
            author = ctx.message.author
            embed = discord.Embed(colour=author.colour)
            embed.set_thumbnail(url=author.avatar_url)
            embed.add_field(name='Joined at', value=author.joined_at, inline=True)
            embed.add_field(name='Nickname', value=author.nick if author.nick else 'N/A', inline=True)
            embed.add_field(name='Status', value=author.status, inline=True)
            embed.add_field(name='Animated Avatar', value='Yes' if author.is_avatar_animated() else 'No', inline=True)

            roles = []
            for role in author.roles:
                roles.append(role.name)
            roles.pop(0)

            embed.add_field(name='Roles', value='N/A' if len(roles) == 0 else ', '.join(roles), inline=True)
            await ctx.send(content='ℹ About **yourself**!', embed=embed)
        else:
            embed = discord.Embed(colour=member.colour)
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name='Joined at', value=member.joined_at, inline=True)
            embed.add_field(name='Nickname', value=member.nick if member.nick else 'N/A', inline=True)
            embed.add_field(name='Status', value=member.status, inline=True)
            embed.add_field(name='Animated Avatar', value='Yes' if member.is_avatar_animated() else 'No', inline=True)

            roles = []
            for role in member.roles:
                roles.append(role.name)
            roles.pop(0)

            embed.add_field(name='Roles', value='N/A' if len(roles) == 0 else ', '.join(roles), inline=True)
            await ctx.send(content=f'ℹ About **{member.display_name}**', embed=embed)


def setup(bot):
    bot.add_cog(Information(bot))
