import discord
from discord import app_commands
from discord.ext import commands

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