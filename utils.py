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

async def allowedChannel(ctx : discord.channel.TextChannel)->bool:
	if type(ctx) is discord.ext.commands.context.Context:
		ctx = ctx.channel
	
	if not (type(ctx) is discord.channel.TextChannel):
		try:
			ctx = ctx.channel
		except:
			return True
	
	if ctx.name not in Bot.ALLOWED_CHANNELS:
		await ctx.send(f"Please use one of the following channel for commands: {formatAllowedChannel(Bot.ALLOWED_CHANNELS)}")
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
	return random.choice(tmpList)

def formatKeys(d : dict):
	out = "["
	for k in d.keys():
		out += str(k) + ","
	if len(d.keys()) != 0:
		out = out[:-1]
	out += "]"
	return out