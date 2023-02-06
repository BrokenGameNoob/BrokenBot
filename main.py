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


	ROLE_SELECTOR_MSG_ID = os.getenv('ROLE_SELECTOR_MSG_ID')
	if ROLE_SELECTOR_MSG_ID != None:
		Bot.ROLE_SELECTOR_MSG_ID = int(ROLE_SELECTOR_MSG_ID)
	ROLE_SELECTOR_MSG_CHANNEL_ID = os.getenv('ROLE_SELECTOR_MSG_CHANNEL_ID')
	if ROLE_SELECTOR_MSG_CHANNEL_ID != None:
		Bot.ROLE_SELECTOR_MSG_CHANNEL_ID = int(ROLE_SELECTOR_MSG_CHANNEL_ID)

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