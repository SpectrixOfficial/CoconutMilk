from discord.ext import commands
import discord
import json

bot = commands.Bot(command_prefix="cm.")
modules = [

]

def main():

    with open("config.json") as f:
        bot.config = json.load(f)

    for module in modules:
        bot.load_extension(module)

    bot.run(bot.config["app"]["token"])
