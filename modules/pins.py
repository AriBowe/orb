import json, asyncio
import discord
from datetime import datetime, timedelta
from discord.ext import commands
import utils.logger

modDef = json.loads("""{
    "type": "pins",
    "name": "Pushpin",
    "requires": [
    ],
    "provides": [
    ]
}""")

log = utils.logger.register(modDef['type'])

class PinModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.pins_store = []
        self.active_servers = []
        self.data = json.load(open("config/pins_config.json"))

        for server in self.data:
            self.active_servers.append(int(server))

        log(f"Initialisation successful, currently watching: {self.active_servers}")

    # Detects pin reactions
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        ctx = reaction.message

        is_pushpin = "📌" == str(reaction.emoji)
        guild_id = ctx.guild.id
        reaction_count = reaction.count
        
        if (is_pushpin 
                and guild_id in self.active_servers
                and ctx.id not in self.pins_store
                and (ctx.channel.id not in self.data[str(guild_id)]['pin_channels']
                and ctx.channel.id not in self.data[str(guild_id)]['excluded_channels'])):
            
            # Target channel selector
            if str(ctx.channel.id) in self.data[str(guild_id)]['channel_switches']:
                target_channel = self.data[str(guild_id)]['channel_switches'][str(ctx.channel.id)]
            else:
                target_channel = 0

            # Pin it
            if reaction_count >= self.data[str(guild_id)]['reaction_counts'][target_channel]:
                self.pins_store.append(ctx.id)
                await self._pin_message(ctx, guild_id, int(self.data[str(guild_id)]['pin_channels'][target_channel]))

    # Actual main pin function
    async def _pin_message(self, ctx, guild_id, pin_channel):
        message_id = ctx.id

        # Checks if the message has already been pinned. Due to how Discord deals with messages,
        # we can ignore messages older than the current bot instance
        if str(message_id) in self.pins_store:
            return
            
        message = discord.Embed(title=ctx.author.display_name, description=str(ctx.content))
        try:
            message.set_thumbnail(url=ctx.author.avatar.url)
        except:
            try:
                message.set_thumbnail(url=ctx.embeds[0].author.avatar.url)
            except:
                pass

        message.set_footer(text=(ctx.created_at + timedelta(hours=10)).strftime("%d %b %Y at %I:%M%p AEST"))

        files = []
        for item in ctx.attachments:
            files.append(await item.to_file())

        view = discord.ui.View(timeout=None)
        view.add_item(discord.ui.Button(label="Context", url=ctx.jump_url, emoji="👁"))

        try:
            await self.bot.get_channel(pin_channel).send(files=files, view=view, embeds=[message, ctx.embeds[0]])
        except: 
            await self.bot.get_channel(pin_channel).send(embeds=[message], view=view, files=files)
    
async def setup(bot):
    await bot.add_cog(PinModule(bot))