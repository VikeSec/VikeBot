import asyncio
import datetime
import os
import sys

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from discord.ext.commands import Cog

import config

from .utils.info import memory, py_ver, uptime


class ForwardOutput(object):
    def __init__(self, bot):
        self.bot = bot

    def write(self, data):
        if len(data) <= 1:
            return
        channel = self.bot.get_channel(config.stage_channel)
        loop = asyncio.get_event_loop()
        loop.create_task(channel.send(f"```bash\n{data}\n```"))


class Stage(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        self.stdout, self.stderr = sys.stdout, sys.stderr
        sys.stdout = sys.stderr = ForwardOutput(self.bot)

        channel = self.bot.get_channel(config.stage_channel)
        await channel.purge(limit=250)

        await channel.send(embed=self.info_embed())

        await asyncio.sleep(config.staging_timeout)

        await channel.send(embed=self.info_embed())
        await self.handle_shudown()

    stage = SlashCommandGroup("stage", "StageBot commands")

    @stage.command(description="Shutdown StageBot")
    async def shutdown(self, ctx: commands.Context):
        await ctx.respond(embed=self.info_embed())
        await self.handle_shudown()

    async def handle_shudown(self):
        sys.stdout, sys.stderr = self.stdout, self.stderr
        await self.bot.shutdown()

    def info_embed(self):
        embed = discord.Embed(title="StageBot Status")
        embed.add_field(
            name="Memory",
            value=f"```py\n{memory()}```",
            inline=True,
        )
        embed.add_field(
            name="Python Version",
            value=f"```py\n{py_ver()}```",
            inline=True,
        )
        embed.add_field(
            name="Uptime",
            value=f"```\n{uptime(self.bot.start_time)}```",
            inline=True,
        )
        embed.set_footer(text=config.bot_name, icon_url=self.bot.user.avatar.url)
        embed.timestamp = datetime.datetime.utcnow()
        embed.color = discord.Color.dark_green()
        return embed


def setup(bot):
    if os.environ.get("BOT_ENV", "") != "staging":
        return

    bot.add_cog(Stage(bot))
