import os

from utils.vikebot import Vikebot

bot = Vikebot()

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        bot.log.info(f"Loaded cog {filename[:-3]}")

bot.run(os.getenv("BOT_TOKEN"))
