import discord
from discord.ext import commands

class CFTTime(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    @commands.group()
    async def ctftime(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(
                title="CTFTime Commands",
                description="Please use one of the following subcommands:",
                color=discord.Color.blue()
            )
            embed.add_field(name="upcoming", value="Show upcoming CTF events.", inline=False)
            embed.add_field(name="details [event_id]", value="Show details of a CTF event with the specified ID.", inline=False)
            await ctx.send(embed=embed)

    @ctftime.command()
    async def upcoming(self, ctx):
        await ctx.send('Upcoming CTF events: ...')

    @ctftime.command()
    async def details(self, ctx, event_id: int):
        await ctx.send(f'Details for CTF event with ID {event_id}: ...')

    
def setup(bot):
    bot.add_cog(CFTTime(bot))
