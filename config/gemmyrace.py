from discord.ui import Select,View;
import discord;
import random;
import config.constants as const;
import requests;


class MySelectRace(View):
    def __init__(self,ctx,amount,wallet_balance,bank_balance,client):
        View.__init__(self)
        self.ctx = ctx
        self.amount = amount
        self.wallet_balance = wallet_balance
        self.bank_balance = bank_balance
        self.client = client
    @discord.ui.select(placeholder="Choose your Gemmy!",
            options=[
                discord.SelectOption(
                    label="Gemmy#921",
                    emoji="<:921:992093550772760647>",
                    description="Gemmy#921 is a swimmer."
                    ),
                discord.SelectOption(
                    label="Gemmy#1456",
                    emoji="<:1456:992093539360051281>",
                    description="Gemmy#1456 is a diver"
                    ),
                discord.SelectOption(
                    label="Gemmy#1669",
                    emoji="<:1669:992093541742415882>",
                    description="Gemmy#1669 is smart and fast"
                    ),
                discord.SelectOption(
                    label="Gemmy#2495",
                    emoji="<:2495:992093547069186078>",
                    description="Gemmy#2495 is a trickster"
                    ),
                discord.SelectOption(
                    label="Gemmy#4634",
                    emoji="<:4634:992093544238034975>",
                    description="Gemmy#4634 smokes Weed"
                    )
            ],
            )
    async def callback(self,interaction,select):
        try:
            if(self.ctx.author==interaction.user):
                select.disabled = True
                em = discord.Embed(title = f"Gemmy Race",color =discord.Color.green())
                await interaction.response.edit_message(view=self)
                # info_message = f"""You have selected {select.values[0]}"""
                em.add_field(name="Gemmy Selected", value=f" {select.values[0]} :",inline=False)
                info_message= ""
                gemmy_list = ["Gemmy#921","Gemmy#1456","Gemmy#4634","Gemmy#1669","Gemmy#2495"]
                winner_gemmy = random.randrange(0,4)
                info_message = " ".join([info_message,f"""\nAnd {gemmy_list[winner_gemmy]} has won the race."""])
                if select.values[0]!=gemmy_list[winner_gemmy]:
                    em.add_field(name="Result",value = "Loose")
                    em.add_field(name="Gems", value=f" {self.amount * 5} :moneybag:",inline=False)
                    # info_message = " ".join([info_message,f"""\nResult : Lose, You lose {self.amount} gems."""])
                    info_message = " ".join([info_message,f"""\nWinning a race will grant you five times the gems you bet."""])
                    self.wallet_balance = self.wallet_balance-self.amount
                else:
                    em.add_field(name="Result",value = "Win")
                    # info_message = " ".join([info_message,f"""\nResult : Win, Congrulations!! You won {self.amount * 5} gems."""])
                    em.add_field(name="Gems", value=f" {self.amount * 5} :moneybag:",inline=False)
                    self.wallet_balance = self.wallet_balance+(self.amount * 5)
                if(self.wallet_balance<0 or self.bank_balance<0):
                    print("There was a impossible Error in deposit_withdraw_gem")
                    raise Exception
                account_json = {"userId":self.ctx.author.id,"walletBalance":self.wallet_balance,"bankBalance":self.bank_balance}
                headers = {"GEMMY_ACCESS_TOKEN":const.GEMMY_ACCESS_TOKEN,"Content-Type": "application/json; charset=utf-8"}
                requests.put(const.UPDATE_BALANCE, json=account_json,headers=headers)
                
                # em.description(info_message)
                em.add_field(name="Wallet Balance",value = self.wallet_balance)
                em.add_field(name="Bank Balance",value = self.bank_balance)
                await interaction.followup.send(embed=em)
            else:
                info_message = f"""Sorry You are not playing this game type '!gemmy bet race amount' to play"""
                em = discord.Embed(title = f"Info",color =discord.Color.red(),description=info_message)
                
                await interaction.response.send_message(embed=em,ephemeral=True)
            # await interaction.response.followup.send(f"""hihihihi {select.values}""")
            # await interaction.response.FollowupMessage(f"You choosed {select.values}")


            return interaction
        except Exception as e:
            print("error in calll back",e)
        
