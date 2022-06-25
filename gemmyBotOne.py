import discord;
from discord.ext import commands;
import config.constants as const;
import json;
import random;
from gemmyBotOneFun import open_account,get_balance,earn_gem,SPS;

client = commands.Bot(command_prefix='!gemmy ')
# os.chdir("X:\GemmyBot-1-Online\economy")






@client.event
async def on_ready():
    print("Started")
    await client.change_presence(status=discord.Status.online,activity=discord.Game("Gemmy Game"))


@client.event
async def on_message(message):
    if message.author==client.user:
        if message.content=="Hello! Welcome to GemmyBotClub. We are Glad You came to visit.":
            await message.add_reaction('\U0001F917')
        return
    if message.content.startswith("hello") or message.content.startswith("Hello") or message.content.startswith("Hi") or message.content.startswith("hi"):
        await message.channel.send ("Hello! Welcome to GemmyBotClub. We are Glad You came to visit.")
    await client.process_commands(message)


@client.event
async def on_message_edit(before, after):
    if after.content =='hi' or after.content == "Hi" or after.content == "Hello" or after.content =="hello":
        await before.channel.send(
            "Hello! Welcome to GemmyBotClub. We are Glad You came to visit."
        )

@client.event
async def on_reaction_add(reaction, user):
    if user==client.user:
        return
    if user == reaction.message.author:
        print(reaction.message)
        await reaction.message.channel.send(f"{user} chosed {reaction.emoji}")


# ==================================================================================================================================#
@client.command()
async def test(ctx, arg):
    await ctx.send(arg)

@client.command()
async def balance(ctx):
    try:
        await open_account(ctx.author)
        balance = await get_balance(ctx.author.id)
        wallet_amount,bank_amount = balance['wallet_balance'],balance['bank_balance']
        em = discord.Embed(title = f"{ctx.author.name}'s balance",color =discord.Color.red())
        em.add_field(name="Wallet Balance",value = wallet_amount)
        em.add_field(name="Bank Balance",value = bank_amount)
        await ctx.send(embed = em)
    except:
        print("error in balance")




@client.command()
async def earn(ctx):
    await open_account(ctx.author)
    earnings_message = await earn_gem(ctx.author.id)
    em = discord.Embed(title = f"{ctx.author.name}'s earnings",color =discord.Color.red(),description=earnings_message)
    await ctx.send(embed = em)


@client.command()
async def bet(ctx,game_name):
    if game_name=="SPS":
        SPS(ctx)







