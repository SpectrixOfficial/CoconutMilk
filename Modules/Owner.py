from discord.ext import commands
import discord
import io
import textwrap
import traceback
from contextlib import redirect_stdout

class Owner:
    """Special commands that only the developer can access."""

    def __init__(self, bot):
        self.bot = bot
        self._last_result = None

    async def __local_check(self, ctx):
        return await self.bot.is_owner(ctx.author)

    def _cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        return content.strip('` \n')

    @commands.command(hidden=True, name='load')
    async def _load(self, ctx, extension):
        self.bot.load_extension(f'Modules.{extension}')
        emb = discord.Embed(color=discord.Colour.from_rgb(135, 0, 117)).set_footer(text=f"🔨 Loaded {extension}")
        await ctx.send(emb)

    @commands.command(hidden=True, name='unload')
    async def _unload(self, ctx, extension):
        self.bot.load_extension(extension)
        emb = discord.Embed(color=discord.Colour.from_rgb(135, 0, 117)).set_footer(text=f"🔨 Unloaded {extension}")
        await ctx.send(emb)

    @commands.command(hidden=True, name='reload')
    async def _reload(self, ctx, extension):
        self.bot.unload_extension(extension)
        self.bot.load_extension(extension)
        emb = discord.Embed(color=discord.Colour.from_rgb(135, 0, 117)).set_footer(text=f"🔨 Reloaded {extension}")
        await ctx.send(emb)

    @commands.command(hidden=True, name='eval')
    async def _eval(self, ctx, *, code: str):
        """Runs Python 3.7 code inside the bot."""

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

        code = self._cleanup_code(code)
        stdout = io.StringIO()

        compile_later = f'async def cmdeval():\n{textwrap.indent(code, "    ")}'

        try:
            exec(compile_later, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}```')

        cmdeval = env['cmdeval']

        try:
            with redirect_stdout(stdout):
                ret = await cmdeval()

        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\N{WHITE HEAVY CHECK MARK}}')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')


def setup(bot):
    bot.add_cog(Owner(bot))
