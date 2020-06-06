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


async def say_permissions(ctx, member, channel):
        permissions = channel.permissions_for(member)
        e = discord.Embed(colour=member.colour)
        avatar = member.avatar_url_as(static_format='png')
        e.set_author(name=str(member), url=avatar)
        allowed, denied = [], []
        for name, value in permissions:
            name = name.replace('_', ' ').replace('guild', 'server').title()
            if value:
                allowed.append(name)
            else:
                denied.append(name)

        e.add_field(name='権限有り', value='\n'.join(allowed))
        e.add_field(name='権限無し', value='\n'.join(denied))
        await ctx.send(embed=e)

    
async def permissions(self, ctx, member: discord.Member = None, channel: discord.TextChannel = None):
    channel = channel or ctx.channel
    if member is None:
        member = ctx.author

    await self.say_permissions(ctx, member, channel)