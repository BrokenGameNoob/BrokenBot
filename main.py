import os
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands

from globalVar import *

from TC2 import TCData_t

from commands import *
from events import *

def main():
	load_dotenv("envConf.env")
	TOKEN = os.getenv('DISCORD_TOKEN')

	# #open text file
	# text_file = open("tmp.txt", "w")

	# tmp = ""
	# vList = tcData.vehicles()
	# for v in vList.values():
	# 	tmp += f"{v.brand.name} {v.name}\n"

	# #write string to file
	# text_file.write(tmp)
	# #close file
	# text_file.close()

	bot.run(TOKEN)



if __name__ == "__main__":
	main()