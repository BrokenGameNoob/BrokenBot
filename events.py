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


@bot.event
async def on_raw_reaction_add(payload=None):
	if payload.user_id == bot.user.id:
		return

	msgID = Bot.ROLE_SELECTOR_MSG_ID
	guild = discord.utils.get(bot.guilds)
	if payload == None:
		return
	if payload.message_id != msgID:
		return
	
	emo = str(payload.emoji)
	for r in Bot.ROLES:
		if emo == r.emojiStr:
			role = discord.utils.get(guild.roles, name=r.roleName)
			if role == None:
				print("Cannot add unknown role: ",r.roleName)
				return
			await payload.member.add_roles(role)

@bot.event
async def on_raw_reaction_remove(payload=None):
	if payload.user_id == bot.user.id:
		return

	msgID = Bot.ROLE_SELECTOR_MSG_ID
	guild = discord.utils.get(bot.guilds)
	if payload is not None:
		if payload.message_id != msgID:
			return

		emo = str(payload.emoji)
		if emo == None:
			return
		for r in Bot.ROLES:
			if emo == r.emojiStr:
				role = discord.utils.get(guild.roles, name=r.roleName)
				if role == None:
					print("Cannot add unknown role: ",r.roleName)
					return
				member = guild.get_member(payload.user_id)
				if member == None:
					print("Can't find member")
				await member.remove_roles(role)