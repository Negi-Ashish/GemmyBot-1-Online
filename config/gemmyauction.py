from typing import Optional
import discord;
from discord.ui import TextInput, Modal



# class Questionnaire(ui.Modal,title="Auction"):
#     # def __init__(self,title: str = ..., timeout: Optional[float] = None, custom_id: str = ...) -> None:
#     #     super().__init__(title=title,timeout=timeout)
#     #     # self.client = client
#     #     # self.ctx = ctx
#     print("one")
#     name = ui.TextInput(label="bid",style= discord.TextStyle.short,placeholder='amount',default='200',max_length=10)
#     # answer = ui.TextInput(label='Answer', style=discord.TextStyle.paragraph)
#     print("two")


#     async def on_submit(self, interaction: discord.Interaction):
#         print("three")
#         await interaction.response.send_message(f'Thanks for your response, {self.name}!', ephemeral=True)


class MyModal(Modal):
    def __init__(self) -> None:
        super().__init__() #title of the modal up top
        self.add_item(TextInput(label="Short Input", placeholder="Placeholder")) 
        self.add_item(
            TextInput(
                label= "Long Input", 
                value= "Default", #sort of like a default
                style=discord.TextStyle.long, #long/short
            )
        )

    async def callback(self, interaction: discord.Interaction):
        embed = discord.Embed(title="Your Modal Results", color=discord.Color.blurple())
        embed.add_field(name="First Input", value=self.children[0].value, inline=False)
        embed.add_field(name="Second Input", value=self.children[1].value, inline=False)
        await interaction.response.send_message(embeds=[embed])
