import datetime
import os

import discord
from discord.commands import SlashCommandGroup
from discord.ext import commands
from discord.ext.commands import Cog

import config


class Stage(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(config.stage_channel)
        await channel.purge(limit=10000)

    stage = SlashCommandGroup("stage", "StageBot commands")

    @stage.command(description="Shutdown StageBot")
    async def shutdown(self, ctx: commands.Context):
        await ctx.respond(embed=await self.shutdown_embed())
        await self.bot.close()

    async def shutdown_embed(self):
        uptime = str(datetime.datetime.utcnow() - self.bot.start_time)[2:][:5]
        embed = discord.Embed(title="StageBot Shutting Down")
        embed.add_field(
            name="Uptime",
            value=f"```{uptime}```",
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
