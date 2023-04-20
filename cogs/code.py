from discord.commands import SlashCommandGroup
from discord.ext import commands

from pyston import PystonClient, File
from pyston.exceptions import *

class Code(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    code = SlashCommandGroup("code", "Code commands")

    @code.command(description="Execute code")
    async def execute(self, ctx, language: str, input: str):
        client = PystonClient()

        language = convert_language_alias(language)

        # Check if language is valid
        try:
            await client.get_runtimes(language)
        except InvalidLanguage:
            await ctx.respond("Invalid language")
            return

        # Execute code
        try:
            result = await client.execute(language, [File(input)])
        except ExecutionError as ex:
            result = ex
        except TooManyRequests:
            await ctx.respond("Too many requests. Please slow down")
            return
        except (InternalServerError, UnexpectedError):
            await ctx.respond("An unknown error has occured ¯\_(ツ)_/¯")

        await ctx.respond(f'```{language}\n{input}```\n```{result}```')

# Convert language to a format that works in both Piston and Discord code blocks 
def convert_language_alias(lang):
    if lang.lower() == 'c#':
        return 'csharp'
    if lang.lower() == 'cplusplus':
        return 'c++'
    return lang.lower()

def setup(bot):
    bot.add_cog(Code(bot))
