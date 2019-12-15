import discord
import mimetypes
import requests
import random

from io import BytesIO
from utils import permissions, http
from discord.ext.commands import errors


class RedditPost:
    """
    Represents a single reddit post with the following attributes:


    (str) subreddit: the subreddit that the post belongs to
    (str) title: the title of the post
    (str) author: the author of the post
    (str) url: link to the image within the reddit post
    (bool) nsfw: whether or not the post is flagged for NSFW content
    (int) upvotes: the number of upvotes
    """
    def __init__(self, subreddit, title, author, url, nsfw, upvotes):
        self.subreddit = subreddit
        self.title = title
        self.author = author
        self.url = url
        self.nsfw = nsfw
        self.upvotes = upvotes

    def get_subreddit(self):
        return self.subreddit

    def get_title(self):
        return self.title

    def get_author(self):
        return self.author

    def get_url(self):
        return self.url

    def get_nsfw(self):
        return self.nsfw

    def get_upvotes(self):
        return self.upvotes

    def __str__(self):
        return '%s %s %s %s %s %d' % (
            self.subreddit,
            self.title,
            self.author,
            self.url,
            self.nsfw,
            self.upvotes,
        )


def _get_rand_post(json_url):
    """Parses the JSON data and returns a RedditPost object corresponding to a random post."""

    all_post_data = requests.get(url=json_url,
                                headers={'user-agent': 'created by Paigekins'}
                                ).json()['data']['children']

    if all_post_data is None:
        raise ValueError('No posts in subreddit.')

    finding_post = True
    while finding_post:
        try:
            rand_post = all_post_data[random.choice([
                i for i in range(len(all_post_data))
            ])]['data']

            post_obj = RedditPost(
                rand_post['subreddit'],
                rand_post['title'],
                rand_post['author'],
                rand_post['url'],
                rand_post['over_18'],
                rand_post['ups']
            )

            finding_post = False

            return post_obj

        except KeyError:
            print('Post could not be parsed. Finding another...')

def _is_image(url):
    """
    Checks whether a normal url contains an image.

    Params:
        (str) url: the url for the image
    Returns:
        (bool): True if url contains an image, False otherwise.
    """
    mimetype, encoding = mimetypes.guess_type(url)
    return (mimetype and mimetype.startswith('image'))


def is_gif(url):
    """Checks if the url contains a gif (not implemented yet)"""
    content_type = requests.head(url).headers['Content-Type']
    pass


def most_upvoted(all_post_data):
    """
    Finds the most upvoted post from some data containing posts (not implemented).

    Params:
        (dict) all_post_data: data on one or more posts
    Returns:
        (dict): data on the most highly upvoted post
    """
    pass


async def create_embed(ctx, post: RedditPost):
    """Creates a tuple with the embed and the chosen random image url"""
    try:
        author = ctx.message.author
        rand_url = post.get_url()
        embed = discord.Embed(
            title=post.get_title(),
            description='**OP**: ' + '/u/' + post.get_author() + '\n **Updoots**: ' + str(post.get_upvotes()) + '\n',
            colour=ctx.me.top_role.colour
        )
        embed.set_footer(text=f'Requested by {author.name}, and retrieved from /r/' + post.get_subreddit() + '.')

        return embed, rand_url

    except AttributeError:
        raise AttributeError('Post parameter must be a RedditPost object.')


async def reddit_imgscrape(ctx, url):
    """
    Randomly selects an image from a subreddit corresponding to a json url and sends it to the channel.
    Checks for permissions, NSFW-mode.

    Params:
        (commands.Context): context
        (str): json url
    """
    current_channel = ctx.message.channel
    author = ctx.message.author

    rand_post = _get_rand_post(url) # RedditPost object

    embed, rand_url = await create_embed(ctx, rand_post)

    lewd_channels = []

    if not permissions.can_attach(ctx):
        await ctx.send('I cannot upload images/GIFs here ;w;')

    for channel in ctx.message.guild.channels:
        if isinstance(channel, discord.VoiceChannel):
            pass
        else:
            if channel.is_nsfw():
                lewd_channels.append(channel)

    if permissions.is_nsfw(ctx):
        try:
            if _is_image(rand_url):
                bio = BytesIO(await http.get(rand_url, res_method='read'))
                extension = rand_url.split('.')[-1]
                await current_channel.send(embed=embed)
                await current_channel.send(file=discord.File(bio, filename='lewd' + '.' + extension))
            else:
                await current_channel.send(embed=embed)
                await current_channel.send(rand_url)
        except KeyError:
            ctx.send('That didn\'t work ;o; please try the command again.')
    else:
        try:
            if not rand_post.get_nsfw():
                if _is_image(rand_url):
                    bio = BytesIO(await http.get(rand_url, res_method='read'))
                    extension = rand_url.split('.')[-1]
                    await current_channel.send(embed=embed)
                    await current_channel.send(file=discord.File(bio, filename='lewd' + '.' + extension))
                else:
                    await current_channel.send(embed=embed)
                    await current_channel.send(rand_url)

            else:
                if lewd_channels:
                    message_str = ''
                    for lewd_channel in lewd_channels:
                        message_str += str(lewd_channel) + '\n'
                    if len(lewd_channels) == 1:
                        await current_channel.send(f'L-lewd {author.name}! NSFW commands go in NSFW-enabled channels!!'
                                           f' This channel is currently NSFW-enabled: \n\n `{message_str}`'
                                           )
                    else:
                        await current_channel.send(f'L-lewd {author.name}! NSFW commands go in NSFW-enabled channels!!'
                                                   f' These channels are currently NSFW-enabled: \n\n `{message_str}`'
                                                   )
                elif not lewd_channels:
                    await current_channel.send(f'L-lewd {author.name}! NSFW commands go in NSFW-enabled channels!!'
                                       ' Unfortunately, though, there are no NSFW-enabled channels in this server ;O;'
                                       )
        except errors.CommandInvokeError:
            ctx.send('Please try the command again. Sometimes the command doesn\'t work for particular posts ;o;')
