from turtle import title
from typing import Optional
from discord import ui
import discord;



class Questionnaire(ui.Modal,title="Auction"):
    custom_id = 123
    def __init__(self,title: str = ..., timeout: Optional[float] = None, custom_id: str = ...) -> None:
        super().__init__(title=title,timeout=timeout, custom_id=custom_id)
        # self.client = client
        # self.ctx = ctx

    name = ui.TextInput(label='Name')
    answer = ui.TextInput(label='Answer', style=discord.TextStyle.paragraph)

    async def on_submit(self, interaction: discord.Interaction):
        
        await interaction.response.send_message(f'Thanks for your response, {self.name}!', ephemeral=True)
