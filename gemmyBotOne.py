from select import select
import discord;
from discord.ext import commands;
from discord.ui import Select,View;
import config.constants as const;
import json;


from gemmyBotOneFun import open_account,get_balance,earn_gem,SPS,check_existance,deposit_withdraw_gem,fortune_teller,RTD;

# client = commands.Bot(command_prefix='!gemmy ')
client = commands.Bot(command_prefix='!gemmy ',intents=discord.Intents.all())
# os.chdir("X:\GemmyBot-1-Online\economy")



@client.event
async def on_ready():
    print("Started")
    await client.change_presence(status=discord.Status.online,activity=discord.Game("Gemmy Games"))


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
@client.command(name="test")
async def test(ctx, arg):
    await ctx.send(arg)

@client.command()
async def balance(ctx):
    try:
        await open_account(ctx.author)
        balance = await get_balance(ctx.author.id)
        wallet_amount,bank_amount = balance['wallet_balance'],balance['bank_balance']
        em = discord.Embed(title = f"{ctx.author.name}'s balance",color =discord.Color.blue())
        em.add_field(name="Wallet Balance",value = wallet_amount)
        em.add_field(name="Bank Balance",value = bank_amount)
        await ctx.send(embed = em)
    except:
        print("error in balance")




@client.command()
async def earn(ctx):
    await open_account(ctx.author)
    earnings_message = await earn_gem(ctx.author.id)
    em = discord.Embed(title = f"{ctx.author.name}'s earnings",color =discord.Color.green(),description=earnings_message)
    await ctx.send(embed = em)


@client.command()
async def bet(ctx,game_name,amount):
    try:
        balance = await get_balance(ctx.author.id)
        wallet_amount,bank_amount = balance['wallet_balance'],balance['bank_balance']
        amount = int(amount)
        if(amount<20):
            info_message = f"""Your bet amount cannot be smaller than 20"""
            em = discord.Embed(title = f" STONE | PAPER | SCISSOR ",color = discord.Color.red(),description=info_message)
            await ctx.send(embed = em)
            return 
        if(amount>wallet_amount):
            info_message = f"""Your bet amount cannot be greater than {wallet_amount}"""
            em = discord.Embed(title = f" STONE | PAPER | SCISSOR ",color = discord.Color.red(),description=info_message)
            await ctx.send(embed = em)
            return 
        if game_name=="SPS":
            await SPS(ctx,client,amount,wallet_amount,bank_amount)
        if game_name=="RTD":
            await RTD(ctx,amount,wallet_amount,bank_amount)
    except:
        info_message = f"""You dont have a account yet. Typle "!gemmy balance" to create one."""
        em = discord.Embed(title = f"Create your free account today!",color = discord.Color.red(),description=info_message)
        await ctx.send(embed = em)




@client.command()
async def deposit(ctx,amount):
    existance = await check_existance(ctx.author.id)
    if existance:
        try:
            amount = int(amount)
            balance = await get_balance(ctx.author.id)
            wallet_amount,bank_amount = balance['wallet_balance'],balance['bank_balance']
            if amount>wallet_amount:
                info_message = f"""Your deposit amount cannot be greater than {wallet_amount}"""
                em = discord.Embed(title = f"Info",color = discord.Color.red(),description=info_message)
                await ctx.send(embed = em)
            else:
                await deposit_withdraw_gem(ctx.author.id,amount,wallet_amount,bank_amount,"deposit")
                info_message = f"""Your have successfully deposited {amount} gem to your bank account, Your current bank balance is {(bank_amount+amount)}"""
                em = discord.Embed(title = f"Deposit Success!",color = discord.Color.red(),description=info_message)
                await ctx.send(embed = em)
        except:
            info_message = """PLease contact MOD for help"""
            em = discord.Embed(title = f"DEPOSIT ERROR",color =discord.Color.red(),description=info_message)
            await ctx.send(embed = em)
    else:
        info_message = """You currently dont have a account. Type '!gemmy balance' to create a account"""
        em = discord.Embed(title = f"Create your free account today!",color =discord.Color.red(),description=info_message)
        await ctx.send(embed = em)


@client.command()
async def withdraw(ctx,amount):
    existance = await check_existance(ctx.author.id)
    if existance:
        try:
            amount = int(amount)
            balance = await get_balance(ctx.author.id)
            wallet_amount,bank_amount = balance['wallet_balance'],balance['bank_balance']
            if amount>bank_amount:
                info_message = f"""Your withdraw amount cannot be greater than {bank_amount}"""
                em = discord.Embed(title = f"Info",color = discord.Color.red(),description=info_message)
                await ctx.send(embed = em)
            else:
                await deposit_withdraw_gem(ctx.author.id,amount,wallet_amount,bank_amount,"withdraw")
                info_message = f"""Your have successfully withdraw {amount} gem to your bank account, Your current bank balance is {(bank_amount-amount)}"""
                em = discord.Embed(title = f"Withdraw Success!",color = discord.Color.red(),description=info_message)
                await ctx.send(embed = em)
        except:
            info_message = """PLease contact MOD for help"""
            em = discord.Embed(title = f"Withdraw ERROR",color =discord.Color.red(),description=info_message)
            await ctx.send(embed = em)
    else:
        info_message = """You currently dont have a account. Type '!gemmy balance' to create a account"""
        em = discord.Embed(title = f"Create your free account today!",color =discord.Color.red(),description=info_message)
        await ctx.send(embed = em)


@client.command()
async def fortune(ctx):
    try:
        balance = await get_balance(ctx.author.id)
        wallet_amount,bank_amount = balance['wallet_balance'],balance['bank_balance']
        if wallet_amount<50:
            info_message = """50 gems are required for knowing your fortune"""
            em = discord.Embed(title = f"Insufficient Balance",color =discord.Color.red(),description=info_message)
            await ctx.send(embed = em)
        else:
            message = await fortune_teller(ctx.author.id,(wallet_amount-50),bank_amount)
            em = discord.Embed(title = f"Your Fortune",color =discord.Color.blue(),description=message)
            await ctx.send(embed = em)

    except:
        info_message = """You currently dont have a account. Type '!gemmy balance' to create a account"""
        em = discord.Embed(title = f"Create your free account today!",color =discord.Color.red(),description=info_message)
        await ctx.send(embed = em)


@client.command()
async def Race(ctx):
    try:
        # balance = await get_balance(ctx.author.id)
        # wallet_amount,bank_amount = balance['wallet_balance'],balance['bank_balance']
        select = Select(
            placeholder="Choose your Gemmy!",
            options=[
                discord.SelectOption(label="Gemmy#921",emoji="<:921:992093550772760647>",description="Gemmy#921 is a professional athlete"),
                discord.SelectOption(label="Gemmy#1456",emoji="<:921:992093550772760647>",description="Gemmy#1456 Never Gives Up"),
                discord.SelectOption(label="Gemmy#1669",emoji="<:921:992093550772760647>",description="Gemmy#1669 is smart and fast"),
                discord.SelectOption(label="Gemmy#2495",emoji="<:921:992093550772760647>",description="Gemmy#2495 is a trickster"),
                discord.SelectOption(label="Gemmy#4634",emoji="<:921:992093550772760647>",description="Gemmy#4634 smokes Weed")
            ]
        )
        view = View()
        view.add_item(select)
        await ctx.send("Choose Your Gemmy!",view=view)

    except Exception as e:
        print(e)
        info_message = """You currently dont have a account. Type '!gemmy balance' to create a account"""
        em = discord.Embed(title = f"Create your free account today!",color =discord.Color.red(),description=info_message)
        await ctx.send(embed = em)

