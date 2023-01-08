from globalVar import *

from utils import *

from TC2 import Vehicle,Brand,TCData_t,getRandomV,VCAT

import asyncio
import re

from discord.ext.commands.context import Context
import threading

import random

async def __deleteMessageFromContext(msgList : list[discord.Message]):
	for m in msgList:
		await m.delete()

async def __delayDelete(msgList : list[discord.Message],delaySec : int):
	await asyncio.sleep(delaySec)
	for m in msgList:
		await m.delete()


@bot.command()
async def ping(ctx):
	if not await allowedChannel(ctx):
		return
	await ctx.channel.send("pong")

def sr(v : Vehicle):
	return v.vcat == VCAT.GROUND.value

@bot.command(name="v")
async def chooseRandomSr(ctx):
	if not await allowedChannel(ctx):
		return
	v = getRandomV(tcData,sr)
	pMsg = ctx.channel.last_message
	msg = await ctx.channel.send(f"{v.brand.name} {v.name} {v.vcat}")
	await __delayDelete([pMsg,msg],60)


#BUG when using a lower case argument
@bot.command(name="r")
async def chooseRandomRace(ctx,*args):
	"""
	Select a random race of a given discipline
	"""
	if not await allowedChannel(ctx):
		return
	eList = tcData.events()
	def filterSr(element):
		if element.discipline != None:
			return element.discipline.name.upper() in args
		return False
	
	pMsg = ctx.channel.last_message
	msg = None
	if len(args) == 0:
		msg = await ctx.channel.send(f"Please use one of the following discipline : { formatKeys(tcData.disciplinesNameMap())}\nExample :\n!r SR\nTo get a Street Race race")
	else:
		e = getRandom(eList,filterSr)
		msg = await ctx.channel.send(f"{e.name}")
	await __delayDelete([pMsg,msg],60)

@bot.command(name="noshi")
async def noshisko(ctx):
	await ctx.channel.send(f"Celui-là ? C'est qui... Connaît personne avec ce nom et une bonne conduite. Celui qui s'en rapproche le plus est <@449349108894007307> mais c'est pas ouf")

@bot.command(name="vote")
async def voteCmd(ctx : discord.ext.commands.context.Context,*args):
	"""
	Create a vote message
	Format a first message with each new option starting on a new line with "X."
	where "X" is a number in [0,10]
	Use !vote to create a vote on the previous message
	"""
	voteCmd : discord.Message = ctx.channel.last_message
	messages = [item async for item in ctx.channel.history(limit=2)]
	if len(messages) < 2:
		return
	target : discord.Message = messages[-1]
	regex = re.compile(r"^(?:\s)*[0-9]*(?:\.)", re.MULTILINE)
	x = regex.findall(target.content)
	await voteCmd.delete()
	if len(x) == 0:
		return
	numList = []
	emojiList = ["0️⃣","1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","🔟"]
	for numStr in x:
		match = re.findall(r"[0-9]+",numStr)[0]
		if len(match) == 0:
			continue
		numList.append(int(match))
		if not numList[-1] in range(0,len(emojiList)):
			await ctx.send(f'Invalid option <{numList[-1]}>')
			return
	for n in numList:
		await target.add_reaction(emojiList[int(n)])
	# await ctx.send(f'{numList}')