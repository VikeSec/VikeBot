import requests
import discord
from discord.ext import commands
from .utils.ctftimeapiutils import fetch_event_info, fetch_upcoming_events

from datetime import datetime, tzinfo

class CFTTime(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.group()
    async def ctftime(self, ctx):
        # Default command that shows a list of subcommands
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="CTFTime Commands",
                color=discord.Color.blue()
            )
            embed.add_field(name="upcoming", value="Show upcoming CTF events.", inline=False)
            embed.add_field(name="details [event_id]", value="Show details of a CTF event with the specified ID.", inline=False)
            await ctx.send(embed=embed)

    @ctftime.command()
    async def upcoming(self, ctx):
        # Get 5 upcoming events
        try:
            events = fetch_upcoming_events(5)
        except requests.exceptions.HTTPError as ex:
            print(f"An error occurred when fetching event info: {ex}")
            return

        # Create an embed for each event
        for event in events:
            embed = discord.Embed(
                title=event["title"],
                color=discord.Color.blue()
            )

            # Convert start time to localtime
            utctime = datetime.fromisoformat(event["start"])
            localtime = utctime.astimezone()
            formatted_time = localtime.strftime(f'%B %d %-l:%M%p')

            embed.add_field(name="Start time", value=formatted_time, inline=False)
            embed.add_field(name="Website", value=event["url"], inline=False)
            embed.add_field(name="Event id", value=event["id"], inline=False)
            await ctx.send(embed=embed)
            

    @ctftime.command()
    async def details(self, ctx, event_id: int):
        await ctx.send(f'Details for CTF event with ID {event_id}: ...')

        try:
            event = fetch_upcoming_events(5)
        except requests.exceptions.HTTPError as ex:
            print(f"An error occurred when fetching event info: {ex}")
            return

    
def setup(bot):
    bot.add_cog(CFTTime(bot))
