from email import message
from http import client
from typing import final
import config.constants as const;
import requests;
import discord;
import random;
from discord.ext import commands;
from config.gemmyrace import MySelectRace
from config.gemmyauction import Questionnaire


async def open_account(user):
    existance = await check_existance(user.id)
    if(existance):
        return False
    else:
        try:
            account_json = {"userId":user.id,"walletBalance":0,"bankBalance":0}
            headers = {"GEMMY_ACCESS_TOKEN":const.GEMMY_ACCESS_TOKEN,"Content-Type": "application/json; charset=utf-8"}
            requests.post(const.ADD_ACCOUNT, json=account_json,headers=headers)
            return True
        except:
            print("There was a Error in adding account")


async def check_existance(userID):
    try:
        api_url = f"""{const.CHECK_ACCOUNT}?userID={userID}"""
        response=requests.get(api_url).json()
        return response['existance']
    except:
        print("There was a Error in getting existance")



async def get_balance(userID):
    try:
        api_url = f"""{const.GET_BALANCE}?userID={userID}"""
        response=requests.get(api_url).json()
        return response
    except:
        print("There was a Error in getting balance")



async def earn_gem(userID):
    try:
        api_url = f"""{const.ACCOUNT_EARN}?userID={userID}"""
        headers = {"GEMMY_ACCESS_TOKEN": const.GEMMY_ACCESS_TOKEN,"Content-Type": "application/json; charset=utf-8"}
        response=requests.put(api_url,headers=headers).json()
        return response['message']
    except:
        print("There was a Error in earn_gem")


async def deposit_withdraw_gem(userID,amount,wallet_balance,bank_balance,method):
    try:
        if method=="deposit":
            bank_balance=bank_balance+amount
            wallet_balance=wallet_balance-amount
        elif method=="withdraw":
            bank_balance=bank_balance-amount
            wallet_balance=wallet_balance+amount
        if(wallet_balance<0 or bank_balance<0):
            print("There was a impossible Error in deposit_withdraw_gem")
            raise Exception
        account_json = {"userId":userID,"walletBalance":wallet_balance,"bankBalance":bank_balance}
        headers = {"GEMMY_ACCESS_TOKEN":const.GEMMY_ACCESS_TOKEN,"Content-Type": "application/json; charset=utf-8"}
        requests.put(const.UPDATE_BALANCE, json=account_json,headers=headers)
        return 
    except:
        print("There was a Error in deposit_withdraw_gem")



async def SPS(ctx,client,amount,wallet_balance,bank_balance):
    try:
        info_message = "\nplease select your choice within 20 seconds."
        em = discord.Embed(title = f" STONE | PAPER | SCISSOR <:3755:994261485649920001>",color =discord.Color.green(),description=info_message)
        message = await ctx.send(embed=em)
        await message.add_reaction('\U0001FAA8')
        await message.add_reaction('\U0001F4F0')
        await message.add_reaction('\U00002702')

        reaction, user = await client.wait_for('reaction_add', check=lambda r, u: u.id == ctx.author.id,timeout=20.0)

        sps = {0:"stone",1:"paper",2:"scissor"}
        bot_sps = sps[random.randrange(0,2)]

        if reaction.emoji=='\U0001FAA8':
            user_played = ":rock:"
            if bot_sps=="stone":
                bot_sps=f":rock:"
                gems = f"""NA"""
                result = "Draw"
            elif bot_sps=="paper":
                bot_sps=f":newspaper:"
                gems = f"""-{amount}"""
                result = "Lose"
            else:
                bot_sps=f":scissors:"
                gems = f"""+{amount}"""
                result="Win"

        elif reaction.emoji=='\U0001F4F0':
            user_played = ":newspaper:"
            if bot_sps=="stone":
                bot_sps=f":rock:"
                gems = f"""+{amount}"""
                result="Win"
            elif bot_sps=="paper":
                bot_sps=f":newspaper:"
                gems = f"""NA"""
                result = "Draw"
            else:
                bot_sps=f":scissors:"
                gems = f"""-{amount}"""
                result = "Lose"

        elif reaction.emoji=='\U00002702':
            user_played=":scissors:"
            if bot_sps=="stone":
                bot_sps=f":rock:"
                gems = f"""-{amount}"""
                result = "Lose"
            elif bot_sps=="paper":
                bot_sps=f":newspaper:"
                gems = f"""+{amount}"""
                result="Win"
            else:
                bot_sps=f":scissors:"
                gems = f"""NA"""
                result = "Draw"

        if result=="Draw":
            result="Draw :slight_smile:"
            pass
        elif result=="Win":
            result = "Win :heart_eyes:"
            wallet_balance=wallet_balance+amount
            await deposit_withdraw_gem(ctx.author.id,0,wallet_balance,bank_balance,"SPS")
        else:
            result="Lose :cry:"
            wallet_balance=wallet_balance-amount
            await deposit_withdraw_gem(ctx.author.id,0,wallet_balance,bank_balance,"SPS")
        
        em = discord.Embed(title = f" STONE | PAPER | SCISSOR <:3755:994261485649920001>",color =discord.Color.green(),description="<:921:992093550772760647> <:1456:992093539360051281> <:1669:992093541742415882>  <:2495:992093547069186078> <:4634:992093544238034975>")
        em.add_field(name=f"{ctx.author.name}",value=user_played,inline=False)
        em.add_field(name="Gemmy ",value=bot_sps,inline=False)
        em.add_field(name="Result",value = f" {result}\n",inline=False)
        em.add_field(name="Gems", value=f" {gems} :moneybag:",inline=False)
        em.add_field(name="Wallet Balance",value = wallet_balance)
        em.add_field(name="Bank Balance",value = bank_balance)
        message = await ctx.send(embed=em)
        
        # use user and reaction
    except:
        sad_messages=["\nGemmy got sad as you didnt play on time.","\nYou always finish quick but today you had to be slow..?","\n I ain't got all day bro.","\n Gemmy is disappointed as you played with its feeling"]
        info_message = sad_messages[random.randrange(0,3)]
        em = discord.Embed(title = f"Penalty (20 gems)",color =discord.Color.red(),description=info_message)
        await deposit_withdraw_gem(ctx.author.id,0,wallet_balance-20,bank_balance,"SPS")
        message = await ctx.send(embed=em)





async def fortune_teller(userID,wallet_balance,bank_balance):
    try:
        await deposit_withdraw_gem(userID,0,wallet_balance,bank_balance,"deduct")
        message = requests.get(const.FORTUNE_TELLER).json()
        return message['message']
    except:
        print("There was a Error in fortune_teller")        


async def RTD(ctx,amount,wallet_balance,bank_balance):
    try:
        em = discord.Embed(title = f" RTD <:3755:994261485649920001>",color =discord.Color.green(),description="<:921:992093550772760647> <:1456:992093539360051281> <:1669:992093541742415882>  <:2495:992093547069186078> <:4634:992093544238034975>")
        bonus=False
        dice_one = random.randrange(1,6)
        dice_two = random.randrange(1,6)
        player_result = dice_one+dice_two
        if(dice_one==dice_two):
            bonus = True
        # info_message = f"""You played {dice_one} and {dice_two} with a total of {player_result}."""
        em.add_field(name="You Rolled",value = f":game_die:{dice_one} --and-- :game_die:{dice_two}",inline=False)
        em.add_field(name="Your Total",value = f"{dice_one+dice_two}",inline=False)
        dice_one = random.randrange(1,6)
        dice_two = random.randrange(1,6)  
        gemmy_result = dice_one+dice_two    
        # info_message = " ".join([info_message,f"""\nGemmy played {dice_one} and {dice_two} with a total of {gemmy_result}."""])
        em.add_field(name="Gemmy Rolled",value = f":game_die:{dice_one} --and-- :game_die:{dice_two}",inline=False)
        em.add_field(name="Gemmy Total",value = f"{dice_one+dice_two}",inline=False)
        if(player_result<gemmy_result):
            wallet_balance=wallet_balance-amount
            await deposit_withdraw_gem(ctx.author.id,0,wallet_balance,bank_balance,"SPS")
            em.add_field(name="Result",value = "Loose :cry:",inline=False)
            em.add_field(name="Gems", value=f" -{amount} :moneybag:",inline=False)
            # info_message = " ".join([info_message,f"""\nResult : Lose, You lose {amount} gems."""])
        elif(player_result>gemmy_result):
            if bonus:
                amount=amount*2
                em.set_footer(text = f"Congrulations!! You got gemmy bonus as you rolled numbers that Gemmy likes!")
                # info_message = " ".join([info_message,f"""\nCongrulations!! You got gemmy bonus as you rolled numbers that Gemmy likes!"""])
            wallet_balance=wallet_balance+amount
            await deposit_withdraw_gem(ctx.author.id,0,wallet_balance,bank_balance,"SPS")
            em.add_field(name="Result",value = "Win :heart_eyes:",inline=False)
            em.add_field(name="Gems", value=f" +{amount} :moneybag:",inline=False)
            # info_message = " ".join([info_message,f"""\nResult : Win, You win {amount} gems."""])
        else:
            em.add_field(name="Result",value = "Draw :slight_smile:",inline=False)
            em.add_field(name="Gems", value=f" 0 :moneybag:",inline=False)
            # info_message = " ".join([info_message,f"""\nResult : Draw, No balance change."""])
        
        em.add_field(name="Wallet Balance",value = wallet_balance)
        em.add_field(name="Bank Balance",value = bank_balance)
        await ctx.send(embed=em)
        
        # use user and reaction
    except:
        info_message = "There was a Error in RTD game please contact any MOD, You will not loose any gems."
        em = discord.Embed(title = f"Info",color =discord.Color.red(),description=info_message)
        message = await ctx.send(embed=em)





async def RACE(ctx,client,amount,wallet_balance,bank_balance):
    try:
        if(amount>200):
            info_message = """You cannot bet more than 200 gems on a race """
            em = discord.Embed(title = f"Info",color =discord.Color.red(),description=info_message)
            await ctx.send(embed = em)
            return
        our_view = MySelectRace(ctx,amount,wallet_balance,bank_balance,client)
        await ctx.send("Choose Your Gemmy!",view=our_view)
        return 

    except Exception as e:
        print(e)
        info_message = """You currently dont have a account. Type '!gemmy balance' to create a account"""
        em = discord.Embed(title = f"Create your free account today!",color =discord.Color.red(),description=info_message)
        await ctx.send(embed = em)


async def fd_gem(userID,amount):
    try:
        api_url = f"""{const.FIXED_DEPOSIT}"""
        headers = {"GEMMY_ACCESS_TOKEN": const.GEMMY_ACCESS_TOKEN,"Content-Type": "application/json; charset=utf-8"}
        account_json = {"userId":userID,"amount":amount}
        response=requests.put(api_url,json=account_json,headers=headers).json()
        return response['message']
    except:
        print("There was a Error in earn_gem")


async def auction(ctx,client):
    try:
        our_view = Questionnaire(ctx,client)
        await ctx.send("Bet amount",view=our_view)
        return 

    except Exception as e:
        print(e)
        info_message = """You currently dont have a account. Type '!gemmy balance' to create a account"""
        em = discord.Embed(title = f"Create your free account today!",color =discord.Color.red(),description=info_message)
        await ctx.send(embed = em)
