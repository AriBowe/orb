"""
This module is based on the amazing work of EvieePy, at https://gist.github.com/EvieePy/ab667b74e9758433b3eb806c53a19f34
"""
import discord
from discord.ext import commands as bot_commands

import asyncio
import itertools
import sys
import traceback
from async_timeout import timeout
from functools import partial
from youtube_dl import YoutubeDL

from cogs.orb_control import allowed_channel

# Settings for ytdl, the module which actually aquires the music
ytdlopts = {
    'format': 'bestaudio/best',
    'outtmpl': 'downloads/%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
    'filter': 'audioonly'
}

# Settings for ffmpeg
ffmpegopts = {
    'before_options': '-nostdin',
    'options': '-vn'
}

ytdl = YoutubeDL(ytdlopts)


class VoiceConnectionError(bot_commands.CommandError):
    """Custom Exception class for connection errors."""


class InvalidVoiceChannel(VoiceConnectionError):
    """Exception for cases of invalid Voice Channels."""


class DownloadError(bot_commands.CommandInvokeError):
    """Exception for cases of invalid Voice Channels."""


class YTDLSource(discord.PCMVolumeTransformer):

    def __init__(self, source, *, data, requester):
        super().__init__(source)
        self.requester = requester

        self.title = data.get('title')
        self.web_url = data.get('webpage_url')

        # YTDL info dicts (data) have other useful information you might want
        # https://github.com/rg3/youtube-dl/blob/master/README.md

    def __getitem__(self, item: str):
        """Allows us to access attributes similar to a dict.
        This is only useful when you are NOT downloading.
        """
        return self.__getattribute__(item)

    @classmethod
    async def create_source(cls, ctx, search: str, *, loop, download=False):
        loop = loop or asyncio.get_event_loop()

        to_run = partial(ytdl.extract_info, url=search, download=download)
        data = await loop.run_in_executor(None, to_run)

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        await ctx.send(f'Added __{data["title"]}__ to the queue.')

        if download:
            source = ytdl.prepare_filename(data)
        else:
            return {'webpage_url': data['webpage_url'], 'requester': ctx.author, 'title': data['title']}

        return cls(discord.FFmpegPCMAudio(source), data=data, requester=ctx.author)

    @classmethod
    async def regather_stream(cls, data, *, loop):
        """Used for preparing a stream, instead of downloading.
        Since Youtube Streaming links expire."""
        loop = loop or asyncio.get_event_loop()
        requester = data['requester']

        to_run = partial(ytdl.extract_info, url=data['webpage_url'], download=False)
        data = await loop.run_in_executor(None, to_run)

        return cls(discord.FFmpegPCMAudio(data['url']), data=data, requester=requester)


class MusicPlayer:
    """A class which is assigned to each guild using the bot for Music.
    This class implements a queue and loop, which allows for different guilds to listen to different playlists
    simultaneously.
    When the bot disconnects from the Voice it's instance will be destroyed.
    """

    __slots__ = ('bot', '_guild', '_channel', '_cog', 'queue', 'next', 'current', 'np', 'volume', 'loop_song')

    def __init__(self, ctx):
        self.bot = ctx.bot
        self._guild = ctx.guild
        self._channel = ctx.channel
        self._cog = ctx.cog

        self.queue = asyncio.Queue()
        self.next = asyncio.Event()

        self.np = None  # Now playing message
        self.volume = .5
        self.current = None
        self.loop_song = False

        ctx.bot.loop.create_task(self.player_loop())

    async def player_loop(self):
        """Our main player loop."""
        await self.bot.wait_until_ready()

        while not self.bot.is_closed():
            self.next.clear()

            try:
                # Wait for the next song. If we timeout cancel the player and disconnect...
                async with timeout(300):  # 5 minutes...
                    source = await self.queue.get()
            except asyncio.TimeoutError:
                return self.destroy(self._guild)

            if not isinstance(source, YTDLSource):
                # Source was probably a stream (not downloaded)
                # So we should regather to prevent stream expiration
                try:
                    source = await YTDLSource.regather_stream(source, loop=self.bot.loop)
                except Exception as e:
                    await self._channel.send(f'There was an error processing your song.\n'
                                             f'```css\n[{e}]\n```')
                    continue

            source.volume = self.volume
            self.current = source

            if self.loop_song:
                self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.current))
            else:           
                try:
                    self._guild.voice_client.play(source, after=lambda _: self.bot.loop.call_soon_threadsafe(self.next.set))
                except AttributeError:
                    print("Playback ended")
            self.np = await self._channel.send(f'**Now Playing:** __{source.title}__ requested by '
                                            f'{source.requester}')
            await self.next.wait()

            # Make sure the FFmpeg process is cleaned up.
            source.cleanup()
            self.current = None

            try:
                # We are no longer playing this song...
                await self.np.delete()
            except discord.HTTPException:
                pass

    def destroy(self, guild):
        """Disconnect and cleanup the player."""
        return self.bot.loop.create_task(self._cog.cleanup(guild))


class Music(bot_commands.Cog):
    """Music related commands."""

    __slots__ = ('bot', 'players')

    def __init__(self, bot):
        self.bot = bot
        self.players = {}
        print("orb_music loaded")

    async def cleanup(self, guild):
        try:
            await guild.voice_client.disconnect()
        except AttributeError:
            pass

        try:
            del self.players[guild.id]
        except KeyError:
            pass

    async def __local_check(self, ctx):
        """A local check which applies to all commands in this cog."""
        if not ctx.guild:
            raise bot_commands.NoPrivateMessage
        return True

    async def __error(self, ctx, error):
        """A local error handler for all errors arising from commands in this cog."""
        if isinstance(error, bot_commands.NoPrivateMessage):
            try:
                return await ctx.send('This command can not be used in Private Messages.')
            except discord.HTTPException:
                pass
        elif isinstance(error, InvalidVoiceChannel):
            await ctx.send('Error connecting to Voice Channel. '
                           'Please make sure you are in a valid channel or provide me with one')
        elif isinstance(error, bot_commands.CommandInvokeError):
            await ctx.send("This command raised an error. Please check the title and resubmit")

        print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
        traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

    def get_player(self, ctx):
        """Retrieve the guild player, or generate one."""
        try:
            player = self.players[ctx.guild.id]
        except KeyError:
            player = MusicPlayer(ctx)
            self.players[ctx.guild.id] = player

        return player

    @bot_commands.command(name='connect', aliases=['join'])
    async def connect_(self, ctx, *, channel: discord.VoiceChannel=None):
        """Connect to voice.
        Parameters
        ------------
        channel: discord.VoiceChannel [Optional]
            The channel to connect to. If a channel is not specified, an attempt to join the voice channel you are in
            will be made.
        This command also handles moving the bot to different channels.
        """
        if not allowed_channel(ctx):
            return

        if not channel:
            try:
                channel = ctx.author.voice.channel
            except AttributeError:
                raise InvalidVoiceChannel('No channel to join. Please either specify a valid channel or join one.')

        vc = ctx.voice_client

        if vc:
            if vc.channel.id == channel.id:
                return
            try:
                await vc.move_to(channel)
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Moving to channel: <{channel}> timed out.')
        else:
            try:
                await channel.connect()
            except asyncio.TimeoutError:
                raise VoiceConnectionError(f'Connecting to channel: <{channel}> timed out.')

        await ctx.send(f'Connected to: **{channel}**')

    @bot_commands.command(name='play', aliases=['add'])
    async def play_(self, ctx, *, search: str):
        """Request a song and add it to the queue.
        This command attempts to join a valid voice channel if the bot is not already in one.
        Uses YTDL to automatically search and retrieve a song.
        Parameters
        ------------
        search: str [Required]
            The song to search and retrieve using YTDL. This could be a simple search, an ID or URL.
        """

        if not allowed_channel(ctx):
            return

        await ctx.trigger_typing()

        vc = ctx.voice_client

        if not vc:
            await ctx.invoke(self.connect_)
            await ctx.trigger_typing()

        player = self.get_player(ctx)

        # If download is False, source will be a dict which will be used later to regather the stream.
        # If download is True, source will be a discord.FFmpegPCMAudio with a VolumeTransformer.
        source = await YTDLSource.create_source(ctx, search, loop=self.bot.loop, download=False)

        await player.queue.put(source)

    # @bot_commands.command(name='remove')   No
    # async def remove_(self, ctx, index: str):
    #     try:
    #         index = int(index)
    #     except TypeError:
    #         await ctx.send("Please enter a number")
    #         return

    #     player = self.get_player(ctx)
    #     await player.queue.get_nowait()

    @bot_commands.command(name='pause')
    async def pause_(self, ctx):
        """Pause the currently playing song."""

        if not allowed_channel(ctx):
            return

        vc = ctx.voice_client

        if not vc or not vc.is_playing():
            return await ctx.send('I am not currently playing anything!')
        elif vc.is_paused():
            return

        vc.pause()
        await ctx.send(f'**`{ctx.author}`**: Paused the song!')

    @bot_commands.command(name="loop", aliases=["repeat"])
    async def loop_(self, ctx):
        """Toggle song looping."""

        if not allowed_channel(ctx):
            return

        player = self.get_player(ctx)
        print(player.loop_song)
    
        if player.loop_song:
            player.loop_song = False
            await ctx.send("Song looping is now disabled")
        else:
            player.loop_song = True
            await ctx.send("Song looping is now enabled")

    @bot_commands.command(name='resume')
    async def resume_(self, ctx):
        """Resume the currently paused song."""

        if not allowed_channel(ctx):
            return

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!')
        elif not vc.is_paused():
            return

        vc.resume()
        await ctx.send(f'**`{ctx.author}`**: Resumed the song!')

    @bot_commands.command(name='skip')
    async def skip_(self, ctx):
        """Skip the song."""

        if not allowed_channel(ctx):
            return

        def skip_check(reaction, user):
            is_skip = "➡" == str(reaction.emoji)
            guild_id = ctx.guild.id
            reaction_count = reaction.count
            return is_skip and reaction_count >= current_limit and guild_id==channel.guild.id

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!')

        if vc.is_paused():
            pass
        elif not vc.is_playing():
            return

        try:
            channel = ctx.author.voice.channel
        except AttributeError:
            raise InvalidVoiceChannel('You are not currently in a voice channel')

        if round(len(channel.members)/3) >= 1:
            current_limit = 1
        else:
            current_limit = round(len(channel.members)/3 + 1)

        react_message = await ctx.send(str(current_limit) + " listeners need to react with ➡ to skip this song! You have 60 seconds to vote")
        await react_message.add_reaction("➡")

        try:
            await self.bot.wait_for('reaction_add', timeout=60.0, check=skip_check)
        except asyncio.TimeoutError:
            await react_message.delete()
        else:
            await react_message.delete()
            vc.stop()
            vc.resume()
            await ctx.send(f'**`{ctx.author}`**: Skipped the song!')


    @bot_commands.command(name='queue', aliases=['q', 'playlist'])
    async def queue_info(self, ctx):
        """Retrieve a basic queue of upcoming songs."""

        if not allowed_channel(ctx):
            return

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!')

        player = self.get_player(ctx)
        if player.queue.empty():
            return await ctx.send('There are currently no more queued songs.')

        current = f"{vc.source.title}"
        upcoming = list(itertools.islice(player.queue._queue, 0, 5))

        embed=discord.Embed(title="SONG QUEUE", color=0xcb410b)
        embed.add_field(name="**Currently playing:** `" + current + "`", value="\u200b")
        i = 1
        for item in upcoming:
            embed.add_field(name="**" + str(i) + ".** `" + str(item["title"]) + "`", value="\u200b", inline=False)
            i += 1

        await ctx.send(embed=embed)

    @bot_commands.command(name='now_playing', aliases=['np', 'current', 'currentsong', 'playing'])
    async def now_playing_(self, ctx):
        """Display information about the currently playing song."""

        if not allowed_channel(ctx):
            return

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!')

        player = self.get_player(ctx)
        if not player.current:
            return await ctx.send('I am not currently playing anything!')

        embed=discord.Embed(title="NOW PLAYING", color=0xcb410b)
        embed.add_field(name="*Currently playing:*", value=f"**{vc.source.title}**\n", inline=False)
        embed.add_field(name="*Requested by:*", value=f'{vc.source.requester}', inline=False)

        await ctx.send(embed=embed)

    @bot_commands.command(name='volume', aliases=['vol'])
    async def change_volume(self, ctx, *, vol = "display"):
        """Change the player volume.
        Parameters
        ------------
        volume: float or int [Required]
            The volume to set the player to in percentage. This must be between 1 and 100.
        """

        if not allowed_channel(ctx):
            return

        vc = ctx.voice_client

        if vol == "display":
            await ctx.send(f'**`{ctx.author}`**: Volume is currently **{vc.source.volume * 100}%**')
            return
        elif vol.isnumeric():
            vol = float(vol)
        else:
            return

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently connected to voice!')

        if not 0 < vol < 101:
            return await ctx.send('Please enter a value between 1 and 100.')

        player = self.get_player(ctx)

        if vc.source:
            vc.source.volume = vol / 100

        player.volume = vol / 100
        await ctx.send(f'**`{ctx.author}`**: Set the volume to **{vol}%**')

    @bot_commands.command(name='stop', aliases=['leave'])
    async def stop_(self, ctx):
        """Stop the currently playing song and destroy the player.
        !Warning!
            This will destroy the player assigned to your guild, also deleting any queued songs and settings.
        """

        if not allowed_channel(ctx):
            return

        vc = ctx.voice_client

        if not vc or not vc.is_connected():
            return await ctx.send('I am not currently playing anything!')

        await self.cleanup(ctx.guild)


def setup(bot):
    bot.add_cog(Music(bot))