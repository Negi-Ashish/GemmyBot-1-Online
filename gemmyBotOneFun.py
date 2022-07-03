from email import message
from http import client
from typing import final
import config.constants as const;
import requests;
import discord;
import random;
from discord.ext import commands;
from config.gemmyrace import MySelectRace



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



async def SPS(ctx,client,amount,wallet_balance,bank_balance):
    try:
        info_message = "\nplease select your choice within 10 seconds."
        em = discord.Embed(title = f" STONE | PAPER | SCISSOR ",color =discord.Color.green(),description=info_message)
        message = await ctx.send(embed=em)
        await message.add_reaction('\U0000270A')
        await message.add_reaction('\U0001F44B')
        await message.add_reaction('\U0000270C')

        reaction, user = await client.wait_for('reaction_add', check=lambda r, u: u.id == ctx.author.id,timeout=10.0)

        sps = {0:"stone",1:"paper",2:"scissor"}
        bot_sps = sps[random.randrange(0,2)]

        if reaction.emoji=='\U0000270A':
            if bot_sps=="stone":
                info_message = f"""\nYou played stone \nGemmy played {bot_sps} \nResult : Draw, No balance change."""
                result = "neutral"
            elif bot_sps=="paper":
                info_message = f"""\nYou played stone \nGemmy played {bot_sps} \nResult : Lose, You lose {amount} gems."""
                result = "lose"
            else:
                info_message = f"""\nYou played stone \nGemmy played {bot_sps} \nResult : Win, You win {amount} gems."""
                result="win"

        elif reaction.emoji=='\U0001F44B':
            if bot_sps=="stone":
                info_message = f"""\nYou played paper \nGemmy played {bot_sps} \nResult : Win, You win {amount} gems."""
                result="win"
            elif bot_sps=="paper":
                info_message = f"""\nYou played paper \nGemmy played {bot_sps} \nResult : Draw, No balance change."""
                result = "neutral"
            else:
                info_message = f"""\nYou played paper \nGemmy played {bot_sps} \nResult : Lose, You lose {amount} gems."""
                result = "lose"

        elif reaction.emoji=='\U0000270C':
            if bot_sps=="stone":
                info_message = f"""\nYou played scissor \nGemmy played {bot_sps} \nResult : Lose, You lose {amount} gems."""
                result = "lose"
            elif bot_sps=="paper":
                info_message = f"""\nYou played scissor \nGemmy played {bot_sps} \nResult : Win, You win {amount} gems."""
                result="win"
            else:
                info_message = f"""\nYou played scissor \nGemmy played {bot_sps} \nResult : Draw, No balance change."""
                result = "neutral"
        if result=="neutral":
            pass
        elif result=="win":
            wallet_balance=wallet_balance+amount
            await deposit_withdraw_gem(ctx.author.id,0,wallet_balance,bank_balance,"SPS")
        else:
            wallet_balance=wallet_balance-amount
            await deposit_withdraw_gem(ctx.author.id,0,wallet_balance,bank_balance,"SPS")
        em = discord.Embed(title = f" STONE | PAPER | SCISSOR ",color =discord.Color.green(),description=info_message)
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



async def fortune_teller(userID,wallet_balance,bank_balance):
    try:
        await deposit_withdraw_gem(userID,0,wallet_balance,bank_balance,"deduct")
        message = requests.get(const.FORTUNE_TELLER).json()
        return message['message']
    except:
        print("There was a Error in fortune_teller")        


async def RTD(ctx,amount,wallet_balance,bank_balance):
    try:
        bonus=False
        dice_one = random.randrange(1,6)
        dice_two = random.randrange(1,6)
        player_result = dice_one+dice_two
        if(dice_one==dice_two):
            bonus = True
        info_message = f"""You played {dice_one} and {dice_two} with a total of {player_result}."""
        dice_one = random.randrange(1,6)
        dice_two = random.randrange(1,6)  
        gemmy_result = dice_one+dice_two    
        info_message = " ".join([info_message,f"""\nGemmy played {dice_one} and {dice_two} with a total of {gemmy_result}."""])
        if(player_result<gemmy_result):
            wallet_balance=wallet_balance-amount
            await deposit_withdraw_gem(ctx.author.id,0,wallet_balance,bank_balance,"SPS")
            info_message = " ".join([info_message,f"""\nResult : Lose, You lose {amount} gems."""])
        elif(player_result>gemmy_result):
            if bonus:
                amount=amount*2
                info_message = " ".join([info_message,f"""\nCongrulations!! You are eligible for a gemmy bonus as you rolled numbers that Gemmy likes!"""])
            wallet_balance=wallet_balance+amount
            await deposit_withdraw_gem(ctx.author.id,0,wallet_balance,bank_balance,"SPS")
            info_message = " ".join([info_message,f"""\nResult : Win, You win {amount} gems."""])
        else:
            info_message = " ".join([info_message,f"""\nResult : Draw, No balance change."""])
        em = discord.Embed(title = f" RTD ",color =discord.Color.green(),description=info_message)
        em.add_field(name="Wallet Balance",value = wallet_balance)
        em.add_field(name="Bank Balance",value = bank_balance)
        await ctx.send(embed=em)
        
        # use user and reaction
    except:
        info_message = "There was a Error in RTD game please contact any MOD, You will not loose any gems."
        em = discord.Embed(title = f"Info",color =discord.Color.red(),description=info_message)
        message = await ctx.send(embed=em)





async def RACE(ctx,amount,wallet_balance,bank_balance):
    try:
        our_view = await MySelectRace()
        await ctx.send("Choose Your Gemmy!",view=our_view)
        a = await our_view.normal_fun()
        print("view",our_view)
        print("a",a)
        return 

    except Exception as e:
        print(e)
        info_message = """You currently dont have a account. Type '!gemmy balance' to create a account"""
        em = discord.Embed(title = f"Create your free account today!",color =discord.Color.red(),description=info_message)
        await ctx.send(embed = em)