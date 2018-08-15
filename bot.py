from discord.ext import commands
import discord
import json

bot = commands.Bot(command_prefix="cm.")
modules = [

]

@bot.event
async def on_ready():
    print(f"{bot.config['name']} {bot.config['version']}")


def main():

    with open("config.json") as f:
        bot.config = json.load(f)

    for module in modules:
        bot.load_extension(f'Modules.{module}')

    bot.run(bot.config["app"]["token"])


if __name__ == '__main__':
    main()
