from datetime import datetime

import discord
import requests
from discord.commands import SlashCommandGroup
from discord.ext import commands

from .utils.ctftimeapiutils import fetch_event_details, fetch_upcoming_events


class CFTTime(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ctftime = SlashCommandGroup("ctftime", "CTFTime commands")

    @ctftime.command(description="Show next 5 upcoming CTFTime events")
    async def upcoming(self, ctx):
        # Get 5 upcoming events
        try:
            events = fetch_upcoming_events(5)
        except requests.exceptions.HTTPError as ex:
            print(f"An error occurred when fetching event info: {ex}")
            await ctx.respond("Sorry, I'm having trouble fetching the upcoming events.")
            return

        # Create an embed for each event
        embeds = []
        for event in events:
            embed = discord.Embed(title=event["title"], color=consistentHash(event["id"]))

            embed.add_field(name="Start", value=ISOToHammerTime(event["start"]))
            embed.add_field(name="Finish", value=ISOToHammerTime(event["finish"]))
            embed.add_field(name="", value="") # Empty field to make two columns
            embed.add_field(name="CTF Website", value=event["url"])
            embed.add_field(name="CTFtime", value=f'[{event["id"]}]({event["ctftime_url"]})')
            embed.add_field(name="", value="") # Empty field to make the rows the same length

            embeds.append(embed)
        
        await ctx.respond(embeds=embeds)

    @ctftime.command(
        description="Show detailed information for an event with the given id"
    )
    async def details(self, ctx, event_id: int):
        try:
            event = fetch_event_details(event_id)
        except requests.exceptions.HTTPError as ex:
            print(f"An error occurred when fetching event info: {ex}")
            await ctx.respond(
                "Sorry, I'm having trouble fetching the details for this event. Are you sure this is a valid event id?"
            )
            return

        embed = discord.Embed(
            title=event["title"],
            description=event["description"],
            color=consistentHash(event["id"])
        )
        embed.set_thumbnail(url=event["logo"])

        # Format organizer
        organizer = f'[{event["organizers"][0]["name"]}](https://ctftime.org/team/{event["organizers"][0]["id"]})'

        embed.add_field(name="Start", value=ISOToHammerTime(event["start"]))
        embed.add_field(name="Finish", value=ISOToHammerTime(event["finish"]))
        embed.add_field(name="Weight", value=event["weight"])
        embed.add_field(name="CTF Website", value=event["url"])
        embed.add_field(name="CTFtime", value=f'[{event["id"]}]({event["ctftime_url"]})')
        embed.add_field(name=f"Organizer", value=organizer)
        embed.add_field(name=f"Restrictions", value=event["restrictions"])
        embed.add_field(name=f"Format", value=event["format"])
        embed.add_field(name=f"Participants", value=str(event["participants"]))
        await ctx.respond(embed=embed)

def consistentHash(txt):
    return int(hex(hash(str(txt)))[3:9], 16)

# Convert a string from ISO format to HammerTime format
def ISOToHammerTime(time):
    utctime = int(datetime.fromisoformat(time).timestamp())
    formatted_time = f"<t:{utctime}:f>"
    return formatted_time

def setup(bot):
    bot.add_cog(CFTTime(bot))
