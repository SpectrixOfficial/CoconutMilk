from discord.ext import commands
import discord
import json
import logging

bot = commands.Bot(command_prefix="cm.")
modules = [
    "Owner"
]
logging.basicConfig(level=logging.INFO)

def main():

    with open("config.json") as f:
        bot.config = json.load(f)

    for module in modules:
        bot.load_extension(f'Modules.{module}')
        print(f"[extensions] loaded {module}")

    bot.run(bot.config["app"]["token"])


if __name__ == '__main__':
    main()
