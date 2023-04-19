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
            ctx.respond("Sorry, I'm having trouble fetching the upcoming events.")
            return

        # Create an embed for each event
        embeds = []
        for event in events:
            embed = discord.Embed(title=event["title"], color=discord.Color.blue())

            # Format start time
            utctime = int(datetime.fromisoformat(event["start"]).timestamp())
            formatted_start_time = f"<t:{utctime}:f>"

            embed.add_field(name="Start time", value=formatted_start_time, inline=False)
            embed.add_field(name="Website", value=event["url"], inline=False)
            embed.add_field(name="Event id", value=event["id"], inline=False)
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
            ctx.respond(
                "Sorry, I'm having trouble fetching the details for this event. Are you sure this is a valid event id?"
            )
            return

        # Format times
        utctime = int(datetime.fromisoformat(event["start"]).timestamp())
        formatted_start_time = f"<t:{utctime}:f>"

        utctime = int(datetime.fromisoformat(event["finish"]).timestamp())
        formatted_finish_time = f"<t:{utctime}:f>"
        # Format duration
        formatted_duration = ""
        if event["duration"]["days"] > 0:
            formatted_duration += f'{event["duration"]["days"]} days '
        if event["duration"]["hours"] > 0:
            formatted_duration += f'{event["duration"]["hours"]} hours'

        embed = discord.Embed(
            title=event["title"],
            description=event["description"],
            color=discord.Color.blue(),
        )
        embed.set_thumbnail(url=event["logo"])

        if len(event["organizers"]) > 1:
            for index, org in enumerate(event["organizers"]):
                embed.add_field(name=f"Organizer {index}", value=org["name"])
                embed.add_field(name=f"Organizer {index} Id", value=org["id"])
        else:
            embed.add_field(name=f"Organizer", value=event["organizers"][0]["name"])
            embed.add_field(name=f"Organizer Id", value=event["organizers"][0]["id"])

        embed.add_field(name=f"Start", value=formatted_start_time)
        embed.add_field(name=f"Finish", value=formatted_finish_time)
        embed.add_field(name=f"Duration", value=formatted_duration)
        embed.add_field(name=f"Website", value=event["url"])
        embed.add_field(name=f"Is votable now", value=str(event["is_votable_now"]))
        embed.add_field(name=f"Restrictions", value=event["restrictions"])
        embed.add_field(name=f"Format", value=event["format"])
        embed.add_field(name=f"Participants", value=str(event["participants"]))
        embed.add_field(name=f"CTFtime URL", value=event["ctftime_url"])
        if event["location"]:
            embed.add_field(name=f"Location", value=event["location"])
        if event["live_feed"]:
            embed.add_field(name=f"Live feed", value=event["live_feed"])
        embed.add_field(name=f"Public votable", value=str(event["public_votable"]))
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(CFTTime(bot))
