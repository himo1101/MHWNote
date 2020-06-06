from discord.ext import commands, tasks
from api import admin
from contextlib import redirect_stdout
from utils import send_embed
import os
import subprocess
import traceback
import discord
import traceback
import io
import textwrap
 
 
 
class Admin(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
 
 
    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])
 
        # remove `foo`
        return content.strip('` \n')
 
    async def cog_check(self, ctx):
        return await self.bot.is_owner(ctx.author)
 
 
    @commands.command()
    async def discord_py(self, ctx):
        await ctx.send(discord.__version__)
 
    @commands.command()
    async def load(self, ctx, module:str, opt:str = None):
        module = f'cogs.{module}'
        if opt is None:
            admin.func_load(bot, module)
 
        elif opt == 'un':
            admin.func_unload(bot, module)

        else:
            return await ctx.message.add_reaction('\N{BLACK QUESTION MARK ORNAMENT}')
        
        await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}')
 
        
    @commands.command()
    async def restart(self, ctx):
        admin.restart()
 
    
    @commands.command(aliases = ['sn'])
    async def send_notice(self, ctx, *, contents: str):
        target = self.bot.get_channel(648878661809733672)
        e = send_embed.defemb(ctx, contents)
        await target.send('@everyone\n', embed = e)
 
   
 
    @commands.command()
    async def cp(self, ctx, member: discord.Member = None, channel: discord.TextChannel = None):
        admin.permissions(member, channel)
 
    @commands.command(aliases = ['role_list'])
    async def _list(self, ctx):
        guild = self.bot.get_guild(619926767821652000)
        desc = '\n'.join(f'{role.name} - {role.id}' for role in reversed(guild.roles))
        embed = discord.Embed(title = '役職一覧', colour = ctx.author.colour, description = desc)
        await ctx.send(embed = embed)
 
    
    @commands.command(name='eval')
    async def _eval(self, ctx, *, body: str = None):
        """Evaluates a code"""
        if body is None:
            return await ctx.send('w')
 
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }
 
        env.update(globals())
        
        body = self.cleanup_code(body)
        stdout = io.StringIO()
        try:
            to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
        func = env['func']
        
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

def setup(bot):
    bot.add_cog(Admin(bot))