from discord.ext import commands;
import config.constants as const;


client2 = commands.Bot(command_prefix='!gemmy')


@client2.command()
async def test(ctx, arg):
    await ctx.send(arg)