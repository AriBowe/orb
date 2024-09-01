import discord, aiohttp
import json, os, re, asyncio, unittest, logging, traceback
from discord.ext import commands

# Load utils
from utils import *
from modules import *

class Orb(commands.Bot):
    client: aiohttp.ClientSession
    def __init__(self, prefix, *args, **kwargs):
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(*args, **kwargs, command_prefix=commands.when_mentioned_or(prefix), intents=intents)

        self.logger = logging.getLogger(self.__class__.__name__)
        self.command_tree_synchronised = False
   
    async def setup_hook(self):
        self.client = aiohttp.ClientSession()

        mods = [f[:-3] for f in os.listdir('modules') if re.match(r'.*[^__]\.py', f)]
        self.logger.info(f"Begining module load. {len(mods)} item(s) detected\n\t\t\t\t------------")
        for mod in mods:
            try:
                await self.load_extension(f"modules.{mod}")
                self.logger.info(f"Module {mod} successfully loaded")
            except:
                self.logger.error(f"Unable to load module {mod} with following error:\n{traceback.format_exc()}")

        if not self.command_tree_synchronised:
            await self.tree.sync()
            self.command_tree_synchronised = True
            self.logger.info("Command tree synchronised")


    async def on_ready(self):
        self.logger.info(f"Established connection to Discord")

def main():
    with open("config/keys.json") as config:
        config = json.load(config)

    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] %(levelname)s: %(message)s")
    bot = Orb(prefix="ob.")
    bot.run(config['keys']['test_token'])

if __name__ == "__main__":
    main()