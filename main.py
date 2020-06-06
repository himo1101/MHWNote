from discord.ext import commands

import botinfo

class MIB(commands.Cog):
    def __init__(self):
        super().__init__(command_prefix = 'm:', description = botinfo.description, help_attrs=dict(hidden=True))

        self.token = botinfo.token
        self.load_extension(f"cogs.start")
 
 
    def default_embed(self, mes: str):
        e = discord.Embed(
            description = mes
        )
        return e
        
 
    async def on_message(self, mes):
        if mes.author.bot:
            return
        await self.process_commands(mes)
 
 
 
    async def start(self):
        await super().start(self.token)
 
    
    def main(self):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.start())
        loop.close()
 
if __name__ == '__main__':
    bot = MIB()
    bot.main()
 