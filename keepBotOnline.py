import discord;
from discord.ext import commands
import config.constants as const

client = commands.Bot(command_prefix='.')


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online,activity=discord.Game("BattlePugs"))

if __name__ == "__main__":
    client.run(const.BOT_TOKEN)