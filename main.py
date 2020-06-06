from discord.ext import commands

import botinfo

class MIB(commands.Cog):
    def __init__(self):
        super().__init__(command_prefix = 'm:', description = botinfo.description, help_attrs=dict(hidden=True))

        self.token = botinfo.token


    async def on_ready(self):
        print("起動しました")