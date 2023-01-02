from globalVar import *

from utils import *

import random

@bot.command()
async def ping(ctx):
	if not await allowedChannel(ctx):
		return
	await ctx.channel.send("pong")

@bot.command(name='99')
async def nine_nine(ctx):
	if not await allowedChannel(ctx):
		return
	brooklyn_99_quotes = [
		'I\'m the human form of the 💯 emoji.',
		'Bingpot!',
		(
			'Cool. Cool cool cool cool cool cool cool, '
			'no doubt no doubt no doubt no doubt.'
		),
	]

	response = random.choice(brooklyn_99_quotes)
	await ctx.send(response)
