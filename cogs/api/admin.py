from discord.ext import commands
import os, subprocess
def func_load(bot, module: str):
    module = 'cogs.{module}'
    try:
        bot.load_extension(module)
    except commands. ExtensionAlreadyLoaded:
        bot.reload_extension(module)


def func_unload(bot, module:str):
    bot.unload_extension(module)


def restart(file_name: str):
    os.system('cals')
    subprocess.run(file_name, shell=True)