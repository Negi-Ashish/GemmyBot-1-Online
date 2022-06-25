import config.constants as const;
import requests;


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
        print(response)
        return response['existance']
    except:
        print("There was a Error in getting existance")



async def get_balance(userID):
    try:
        api_url = f"""{const.GET_BALANCE}?userID={userID}"""
        response=requests.get(api_url)
        return response
    except:
        print("There was a Error in getting existance")

