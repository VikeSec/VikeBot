import datetime
import os

import discord
from discord.ext.commands import Cog

import config


class Stage(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        channel = self.bot.get_channel(config.stage_channel)
        await channel.purge(limit=10000)

    @Cog.listener()
    async def on_command_error(self, ctx, error):
        embed = discord.Embed(title="Error")
        embed.set_thumbnail(
            url = discord.utils.get(ctx.guild.emojis, name="Deny").url
        )
        embed.add_field(
            name="Output",
            value=f"```python\n{error}```",
            inline=False,
        )
        embed.set_footer(text=config.bot_name, icon_url=self.bot.user.avatar)
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.channel.send(embed=embed)
        raise error


def setup(bot):
    if os.environ.get("BOT_ENV", "") != "staging":
        return
    bot.add_cog(Stage(bot))
