import discord
from discord import app_commands
from discord.ext import commands

import random

from globalVar import *

def formatAllowedChannel(channelList)->str:
	out = ""
	for c in channelList:
		out = f"{out}***{c}***,"
	return out[:-1]

async def allowedChannel(msg : discord.Message)->bool:
	ctx = None
	if type(msg) is discord.ext.commands.context.Context:
		ctx = msg.channel
	
	if not (type(msg) is discord.channel.TextChannel):
		try:
			ctx = msg.channel
		except:
			return True
	
	if ctx == None:
		return False
	
	if ctx.name not in Bot.ALLOWED_CHANNELS and msg.content[1:] not in globalCommands:
		await ctx.send(f"{msg.author.mention}, please use one of the following channel for commands: {formatAllowedChannel(Bot.ALLOWED_CHANNELS)}")
		return False

	return True

async def getRole(bot : commands.Bot,roleName : str)->discord.Role:
	guild = discord.utils.get(bot.guilds)
	role = discord.utils.get(guild.roles, name=roleName)
	return role

async def getMessage(channel: discord.TextChannel,id)->discord.Message:
	return await channel.fetch_message(id)

def getRandom(list,filter : callable):
	tmpList = []
	for a in list.values():
		if filter(a):
			tmpList.append(a)
	if len(tmpList) == 0:
		return None
	return random.choice(tmpList)

def formatKeys(d : dict,virtualKeys:list = None):
	"""
	@param virtualKeys: keys non existing in the dict to be added to the formatted output
	"""
	count = len(d.keys()) + len(virtualKeys)
	out = "["
	for k in d.keys():
		out += str(k) + ","
	if virtualKeys != None:
		for vk in virtualKeys:
			out += str(vk) + ","
	if count != 0:
		out = out[:-1]
	out += "]"
	return out