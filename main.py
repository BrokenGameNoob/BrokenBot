import os
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands

from globalVar import *

from commands import *
from events import *

def main():    
	load_dotenv("envConf.env")
	TOKEN = os.getenv('DISCORD_TOKEN')

	bot.run(TOKEN)



if __name__ == "__main__":
	main()