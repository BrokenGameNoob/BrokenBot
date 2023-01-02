from globalVar import *
from utils import *

import random

@bot.event
async def on_message(message):
	if message.author == bot.user:
		return

	ctx = await bot.get_context(message)
	if ctx.valid:
		if not await allowedChannel(message):
			return
	
	await bot.process_commands(message)