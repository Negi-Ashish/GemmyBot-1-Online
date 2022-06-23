from discord.ext import commands;
import config.constants as const;


client2 = commands.Bot(command_prefix='/')

if __name__ == "__main__":
    client2.run(const.TEST_BOT_TOKEN)