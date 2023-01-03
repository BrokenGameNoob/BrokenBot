from globalVar import *

from utils import *

import random

@bot.command()
async def ping(ctx):
	if not await allowedChannel(ctx):
		return
	await ctx.channel.send("pong")


