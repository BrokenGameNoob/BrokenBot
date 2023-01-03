from globalVar import *
from utils import *

import discord
from discord import app_commands
from discord.ext import commands

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


@bot.event
async def on_member_join(member : discord.Member):
	guild = discord.utils.get(bot.guilds)
	print("Member joined! ",member)
	if guild.system_channel:
		roleChannel = bot.get_channel(bot.ROLE_SELECTOR_MSG_CHANNEL_ID)
		if roleChannel == None:
			print(f"Role channel not found ! <{bot.ROLE_SELECTOR_MSG_CHANNEL_ID}>")
			return
		await guild.system_channel.send(
			f"Hi {member.mention}! Please select your language here: {roleChannel.mention}\n"+
			"If you don't do so, you won't get notified when new or announcements are published.\n"+
			"\n"+
			f"Salut {member.mention} ! Merci de sélectionner une langue ici : {mention(Bot.ROLE_SELECTOR_MSG_CHANNEL_ID)}\n"+
			"Cette étape est nécessaire pour être notifié lorsque des informations sont publiées.")