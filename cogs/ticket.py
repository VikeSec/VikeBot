import discord
from discord import ButtonStyle, Interaction, SelectOption
from discord.commands import SlashCommandGroup
from discord.ext.commands import Cog, Context
from discord.ui import Button, View, button, select

import config


class NewTicketOptions(View):
    def __init__(self):
        super().__init__(timeout=None)

    @select(
        custom_id="menu",
        placeholder="How can we help?",
        min_values=1,
        max_values=1,
        options=[
            SelectOption(
                label="Question",
                value="question",
                description="If you have a simple question.",
                emoji="❔",
            ),
            SelectOption(
                label="Help",
                value="help",
                description="If you need help from us.",
                emoji="🔧",
            ),
            SelectOption(
                label="Report",
                value="report",
                description="To report a misbehaving user.",
                emoji="🚫",
            ),
        ],
    )
    async def select_callback(self, select: SelectOption, interaction: Interaction):
        guild = interaction.guild
        category = discord.utils.get(
            interaction.guild.categories, id=config.tickets_category
        )

        if interaction.data.get("values")[0] == "question":

            channel = await guild.create_text_channel(
                name=f"❔┃{interaction.user.display_name}-ticket", category=category
            )

            await interaction.response.send_message(
                f"> The {channel.mention} channel was created to solve your questions.",
                delete_after=3,
            )

            await channel.set_permissions(
                interaction.user,
                send_messages=True,
                read_messages=True,
                add_reactions=True,
                embed_links=True,
                attach_files=True,
                read_message_history=True,
                external_emojis=True,
            )

            embed_question = discord.Embed(
                title=f"Question - Hi {interaction.user.display_name}!",
                description="Please ask your question below.\n\nIf you can't get someone to help you, press the button `🔔 Call staff`..",
                color=0xFFFFFF,
            )
            embed_question.set_thumbnail(url=interaction.user.avatar.url)

            await channel.send(interaction.user.mention, embed=embed_question)
            message = (await channel.history(limit=1, oldest_first=True).flatten())[0]
            # await message.edit(content="TEST123")

class NewTicket(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(
        custom_id="ticket",
        label="Create a ticket",
        style=ButtonStyle.green,
        emoji="🔧",
    )
    async def button_callback(self, button: Button, interaction: Interaction):
        msg = await interaction.response.send_message(
            "Please choose the ticket type",
            view=NewTicketOptions(),
            ephemeral=True,
            delete_after=20,
        )


class Ticket(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        self.bot.add_view(NewTicket())

    ticket = SlashCommandGroup("ticket", "Ticket commands")

    @ticket.command(description="Create new ticket")
    async def init(self, ctx: Context):
        embed = discord.Embed(
            title="Tickets",
            description="Welcome to tickets system.",
            color=0xFCD005,
        )

        await ctx.respond(embed=embed, view=NewTicket())


def setup(bot):
    cog = Ticket(bot)
    bot.add_cog(cog)
