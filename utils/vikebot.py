import logging
from datetime import datetime

import aiohttp
import discord
from discord.ext import commands

import config

log = logging.getLogger("bot.core")
logging.basicConfig(
    level=logging.INFO,
    datefmt="%I:%M %p on %B %d %Y",
    format="%(asctime)s:%(levelname)s: %(name)s: %(message)s",
)


class Vikebot(commands.Bot):
    """
    Main bot subclass
    """

    def __init__(self):
        super().__init__(
            command_prefix=config.command_prefix,
            case_insensitive=True,
            allowed_mentions=discord.AllowedMentions(
                users=True, roles=True, everyone=False, replied_user=False
            ),
            owner_id=config.owner_id,
            description=config.bot_description,
            debug_guilds=config.debug_guilds,
        )

        self.start_time = datetime.utcnow()
        self.session = aiohttp.ClientSession()
        self.footer = config.bot_description
        self.color = 0x003F87
        self.log = log

    def __str__():
        return config.bot_description

    async def on_ready(self):
        print(f"Logged in as {self.user}")

    async def shutdown(self):
        await self.session.close()
        await self.close()
