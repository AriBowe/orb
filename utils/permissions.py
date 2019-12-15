import discord


def can_send(ctx):
    """
    Checks whether the bot can send messages in a channel.

    Params:
        (discord.commands.Context) ctx: context
    Returns:
        (bool): True if bot can send message, False otherwise
    """
    return isinstance(ctx.channel, discord.DMChannel) or ctx.channel.permissions_for(ctx.guild.me).send_messages


def can_embed(ctx):
    """Checks whether bot can send embedded images into current channel"""
    return isinstance(ctx.channel, discord.DMChannel) or ctx.channel.permissions_for(ctx.guild.me).embed_links


def can_attach(ctx):
    """Checks if bot can attach files in their messages."""
    return isinstance(ctx.channel, discord.DMChannel) or ctx.channel.permissions_for(ctx.guild.me).attach_files


def can_connect_voice(ctx):
    """Checks if bot can connect to a voice channel."""
    return isinstance(ctx.channel, discord.DMChannel) or ctx.channel.permissions_for(ctx.guild.me).connect


def is_nsfw(ctx):
    """Checks if the channel has NSFW mode enabled"""
    return isinstance(ctx.channel, discord.DMChannel) or ctx.channel.is_nsfw()


def can_react(ctx):
    """Checks if the bot can react to messages"""
    return isinstance(ctx.chaannel, discord.DMChannel) or ctx.channel.permissions_for(ctx.guild.me).add_reactions
