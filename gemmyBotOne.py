from select import select
import discord;
from discord.ext import commands;

import config.constants as const;
import json;


from gemmyBotOneFun import open_account,get_balance,earn_gem,SPS,check_existance,deposit_withdraw_gem,fortune_teller,RTD,RACE,fd_gem;

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
        wallet_amount,bank_amount,fixed_deposit = balance['wallet_balance'],balance['bank_balance'],balance['fixed_deposit']
        em = discord.Embed(title = f"{ctx.author.name}'s balance <:3755:994261485649920001>",color =discord.Color.blue())
        em.add_field(name="Fixed Deposit",value = fixed_deposit,inline=False)
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
        game_name=game_name.lower()
        balance = await get_balance(ctx.author.id)
        wallet_amount,bank_amount = balance['wallet_balance'],balance['bank_balance']
        amount = int(amount)
        if(amount<20):
            info_message = f"""Your bet amount cannot be smaller than 20"""
            em = discord.Embed(title = f"<:3755:994261485649920001> Info",color = discord.Color.red(),description=info_message)
            await ctx.send(embed = em)
            return 
        if(amount>wallet_amount or amount>1000):
            if amount>1000:
                wallet_amount = 1000
            info_message = f"""Your bet amount cannot be greater than ({wallet_amount}) gems"""
            em = discord.Embed(title = f"<:3755:994261485649920001> Info",color = discord.Color.red(),description=info_message)
            await ctx.send(embed = em)
            return 
        if game_name=="sps":
            await SPS(ctx,client,amount,wallet_amount,bank_amount)
        elif game_name=="rtd":
            await RTD(ctx,amount,wallet_amount,bank_amount)
        elif game_name=="race":
            await RACE(ctx,client,amount,wallet_amount,bank_amount)

    except:
        info_message = f"""You dont have a account yet. Typle "!gemmy balance" to create one."""
        em = discord.Embed(title = f"<:3755:994261485649920001> Create your free account today!",color = discord.Color.red(),description=info_message)
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
                em = discord.Embed(title = f"<:3755:994261485649920001> Info",color = discord.Color.red(),description=info_message)
                await ctx.send(embed = em)
            else:
                await deposit_withdraw_gem(ctx.author.id,amount,wallet_amount,bank_amount,"deposit")
                info_message = f"""Your have successfully deposited {amount} gem to your bank account, Your current bank balance is {(bank_amount+amount)}"""
                em = discord.Embed(title = f"<:3755:994261485649920001> Deposit Success!",color = discord.Color.red(),description=info_message)
                await ctx.send(embed = em)
        except:
            info_message = """PLease contact MOD for help"""
            em = discord.Embed(title = f"DEPOSIT ERROR",color =discord.Color.red(),description=info_message)
            await ctx.send(embed = em)
    else:
        info_message = """You currently dont have a account. Type '!gemmy balance' to create a account"""
        em = discord.Embed(title = f"<:3755:994261485649920001> Create your free account today!",color =discord.Color.red(),description=info_message)
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
                em = discord.Embed(title = f"<:3755:994261485649920001> Info",color = discord.Color.red(),description=info_message)
                await ctx.send(embed = em)
            else:
                await deposit_withdraw_gem(ctx.author.id,amount,wallet_amount,bank_amount,"withdraw")
                info_message = f"""Your have successfully withdraw {amount} gem to your bank account, Your current bank balance is {(bank_amount-amount)}"""
                em = discord.Embed(title = f"<:3755:994261485649920001> Withdraw Success!",color = discord.Color.red(),description=info_message)
                await ctx.send(embed = em)
        except:
            info_message = """PLease contact MOD for help"""
            em = discord.Embed(title = f"<:3755:994261485649920001> Withdraw ERROR",color =discord.Color.red(),description=info_message)
            await ctx.send(embed = em)
    else:
        info_message = """You currently dont have a account. Type '!gemmy balance' to create a account"""
        em = discord.Embed(title = f"<:3755:994261485649920001> Create your free account today!",color =discord.Color.red(),description=info_message)
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
            em = discord.Embed(title = f"Your Fortune <:3755:994261485649920001>",color =discord.Color.blue(),description=message)
            await ctx.send(embed = em)

    except:
        info_message = """You currently dont have a account. Type '!gemmy balance' to create a account"""
        em = discord.Embed(title = f"<:3755:994261485649920001> Create your free account today!",color =discord.Color.red(),description=info_message)
        await ctx.send(embed = em)


@client.command()
async def fd(ctx,amount):
    try:
        await open_account(ctx.author)
        earnings_message = await fd_gem(ctx.author.id,int(amount))
        em = discord.Embed(title = f"Info",color =discord.Color.green(),description=earnings_message)
        em.set_footer(text = f"You can earn maximum of 1500 gems as interest.")
        await ctx.send(embed = em)
    except:
        info_message = """You currently dont have a enough balance to open a FD"""
        em = discord.Embed(title = f"<:3755:994261485649920001> Play with gemmy to Earn!",color =discord.Color.red(),description=info_message)
        await ctx.send(embed = em)

@client.command()
async def info(ctx,command):
    command = command.lower()
    try:
        if command=="balance": 
            info_message = """\nThis command will create a new account for you with wallet balance and bank balance of zero.
                              \nIf you alredy have a account it will display your wallet balance, bank balance and Fixed Deposit amount."""
            em = discord.Embed(title = f"<:3755:994261485649920001> Syntax:`!gemmy balance`",color =discord.Color.blue(),description=info_message)
        elif command=="earn":
            info_message = """\nThis command will let you earn random amount of gems within a interval of 4 hours.
                              \nIf you encounter an error make sure you have created a account first."""
            em = discord.Embed(title = f"<:3755:994261485649920001> Syntax:`!gemmy earn`",color =discord.Color.blue(),description=info_message)

        elif command=="deposit":
            info_message="""\n amount is the number of gems you want to transfer
                            \nThis command will help you to deposit your gems from your wallet to your bank account.
                            \nYou can only transfer amount smaller than equal to your wallet balance."""
            em = discord.Embed(title = f"<:3755:994261485649920001> Syntax:`!gemmy deposit amount`",color =discord.Color.blue(),description=info_message)

        elif command=="withdraw":
            info_message="""\n amount is the number of gems you want to transfer
                            \nThis command will help you to withdraw your gems from your bank to your wallet.
                            \nYou can only transfer amount smaller than equal to your bank balance."""
            em = discord.Embed(title = f"<:3755:994261485649920001> Syntax:`!gemmy withdraw amount`",color =discord.Color.blue(),description=info_message)
        elif command=="bet":
            info_message= """\n game name can be
                             \n"SPS" (STONE PAPER SCISSOR)
                             \n"RACE" (GEMMY RACE)
                             \n"RTD" (ROLL THE DICE)
                             \n amount is the number of gems you want to bet
                            """
            em = discord.Embed(title = f"<:3755:994261485649920001> Syntax:`!gemmy bet game_name amount`",color =discord.Color.blue(),description=info_message)
        elif command=="fortune":
            info_message= """\nThis command will tell you your fortune for 50 gems. """
            em = discord.Embed(title = f"<:3755:994261485649920001> Syntax:`!gemmy fortune`",color =discord.Color.blue(),description=info_message)
        elif command=="fd":
            info_message= """\nThis command will help you start a Fixed Deposit of 3 days.
                             \nYou cannot make a fixed deposit of amount greater than your bank balance.
                             \nOnce you make a FD the amount is transferred to your FD account and locked for 3 days.
                             \nYou cannot break you FD so think before you start one.
                             \nFD gives you interest rate of 6%
                             \nYou cannont earn more than 1500 gems of interest"""
            em = discord.Embed(title = f"<:3755:994261485649920001> Syntax:`!gemmy fd amount`",color =discord.Color.blue(),description=info_message)

        
        await ctx.send(embed = em)
    except:
        info_message = """There was a error in Info"""
        em = discord.Embed(title = f"<:3755:994261485649920001>Info",color =discord.Color.red(),description=info_message)
        await ctx.send(embed = em)