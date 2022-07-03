from discord.ui import Select,View;
import discord;

class MySelectRace(View):
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
    async def select_callback(self,interaction,select):
        try:
            # print("ctx_user",self.author)
            print("user",interaction.user)
            select.disabled = True
            await interaction.response.edit_message(view=self)
            # await interaction.response.followup.send(f"""hihihihi {select.values}""")
            # await interaction.response.FollowupMessage(f"You choosed {select.values}")
            # info_message = f"""this is a test message {select.values}"""
            # em = discord.Embed(title = f"Test",color =discord.Color.green(),description=info_message)

            await interaction.followup.send(f"You choosed {select.values}",ephemeral=True)
        except Exception as e:
            print("error in calll back",e)
            print(interaction.response)
            print(type(interaction))
       
        
