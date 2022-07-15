from typing import Optional
from discord import ui
import discord;



class Questionnaire(ui.Modal,title="Auction"):
    # def __init__(self,title: str = ..., timeout: Optional[float] = None, custom_id: str = ...) -> None:
    #     super().__init__(title=title,timeout=timeout)
    #     # self.client = client
    #     # self.ctx = ctx
    print("one")
    name = ui.TextInput(label='Name',style=discord.TextStyle.short,placeholder="numbers only",required=True)
    # answer = ui.TextInput(label='Answer', style=discord.TextStyle.paragraph)
    print("two")

    
    async def on_submit(self, interaction: discord.Interaction):
        print("three")
        await interaction.response.send_message(f'Thanks for your response, {self.name}!', ephemeral=True)
