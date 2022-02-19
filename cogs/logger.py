import datetime

import discord
from discord.ext import commands

import config


class Logger(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener("on_message_edit")
    async def on_message_edit(self, before, message):
        if not config.bot_name:
            return

        if (
            message.author == self.bot.user
            or message.channel.id == config.logger_channel
            or before.content == message.content
        ):
            return

        embed = discord.Embed(
            title=f"User: {message.author} ({message.author.display_name})"
        )
        embed.set_thumbnail(url=message.author.avatar)
        embed.add_field(
            name="Action",
            value=f"{message.author} updated their message in #{message.channel}\n[Click to view message]({message.jump_url})",
            inline=False,
        )
        embed.add_field(name="From", value=before.content, inline=False)
        embed.add_field(name="To", value=message.content, inline=False)
        embed.add_field(
            name="IDs",
            value=f"```ahk\nUser: {message.author.id}\nMessage: {message.id}```",
            inline=False,
        )
        embed.set_footer(text=config.bot_name, icon_url=self.bot.user.avatar)
        embed.timestamp = datetime.datetime.utcnow()

        channel = self.bot.get_channel(config.logger_channel)
        await channel.send(embed=embed)

    @commands.Cog.listener("on_message_delete")
    async def on_message_delete(self, message):
        if not config.bot_name:
            return

        if (
            message.author == self.bot.user
            or message.channel.id == config.logger_channel
        ):
            return

        embed = discord.Embed(
            title=f"User: {message.author} ({message.author.display_name})"
        )
        embed.set_thumbnail(url=message.author.avatar)
        embed.add_field(
            name="Action",
            value=f"{message.author}'s message was deleted in #{message.channel}",
            inline=False,
        )
        embed.add_field(name="Old Message", value=message.content, inline=False)
        embed.add_field(
            name="IDs",
            value=f"```ahk\nUser: {message.author.id}\nMessage: {message.id}```",
            inline=False,
        )
        embed.set_footer(text=config.bot_name, icon_url=self.bot.user.avatar)
        embed.timestamp = datetime.datetime.utcnow()
        channel = self.bot.get_channel(config.logger_channel)
        await channel.send(embed=embed)


def setup(bot):
    bot.add_cog(Logger(bot))
