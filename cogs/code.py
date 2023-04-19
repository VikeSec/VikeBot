from discord.commands import SlashCommandGroup
from discord.ext import commands

class Code(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    code = SlashCommandGroup("code", "Code commands")

    @code.command(description="Execute code")
    async def execute(self, ctx, input: str):
        
        await ctx.respond("This command will execute the code")
        

def setup(bot):
    bot.add_cog(Code(bot))
