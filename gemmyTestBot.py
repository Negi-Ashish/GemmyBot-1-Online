from discord.ext import commands;
import config.constants as const;
import requests

client2 = commands.Bot(command_prefix='!gemmy ')


@client2.command()
async def test(ctx, arg):
    await ctx.send(arg)


@client2.command()
async def test_api(ctx):
    api_url = "https://gemmy-bot-one-db.herokuapp.com/test_read"
    await requests.get(api_url)