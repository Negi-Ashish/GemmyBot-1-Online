from email import message
import config.constants as const;
import requests;
import discord;
from discord.ext import commands;

async def open_account(user):
    existance = await check_existance(user.id)
    if(existance):
        return False
    else:
        try:
            account_json = {"userId":user.id,"walletBalance":0,"bankBalance":0}
            requests.post(const.ADD_ACCOUNT, json=account_json)
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
        response=requests.put(api_url).json()
        return response['message']
    except:
        print("There was a Error in earn_gem")



async def SPS(ctx):
    try:
        info_message = "STONE | PAPER | SCISSOR   please select your choice."
        em = discord.Embed(title = f" STONE | PAPER | SCISSOR ",color =discord.Color.red(),description=info_message)
        message = await ctx.send(embed=em)
        await message.add_reaction('\U0000270A')
        await message.add_reaction('\U0001F44B')
        await message.add_reaction('\U0000270C')

    except:
        pass



async def deposit_withdraw_gem(userID,amount,wallet_balance,bank_balance,method):
    try:
        if method=="deposit":
            bank_balance=bank_balance+amount
            wallet_balance=wallet_balance-amount
        if method=="withdraw":
            bank_balance=bank_balance-amount
            wallet_balance=wallet_balance+amount
        if(wallet_balance<0 or bank_balance<0):
            print("There was a impossible Error in deposit_withdraw_gem")
            raise Exception
        account_json = {"userId":userID,"walletBalance":wallet_balance,"bankBalance":bank_balance}
        requests.put(const.UPDATE_BALANCE, json=account_json)
        return 
    except:
        print("There was a Error in deposit_withdraw_gem")



async def fortune_teller(userID,wallet_balance,bank_balance):
    try:
        await deposit_withdraw_gem(userID,wallet_balance,bank_balance,"deduct")
        message=requests.get(const.FORTUNE_TELLER)
        return message
    except:
        pass
