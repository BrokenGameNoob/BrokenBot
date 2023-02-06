import discord
from discord import app_commands
from discord.ext import commands

from TC2 import TCData_t

intents = discord.Intents.all()

class Role:
	def __init__(self,emojiStr:str,roleName:str) -> None:
		self.emojiStr = emojiStr
		self.roleName = roleName

async def getRole(bot : commands.Bot,roleName : str)->discord.Role:
	guild = discord.utils.get(bot.guilds)
	role = discord.utils.get(guild.roles, name=roleName)
	return role

async def giveRole(guild : discord.Guild,member : discord.Member,role : Role | discord.Role):
	if isinstance(role,Role):
		role = discord.utils.get(guild.roles, name=role.roleName)
	if role == None:
		print("Cannot add unknown role: ",role.roleName)
		return
	await member.add_roles(role)

class Bot(commands.Bot):

	ALLOWED_CHANNELS = ["bot-mania","🥴mess🥴"]
	ROLE_SELECTOR_MSG_ID = 1059592418875420690
	ROLE_SELECTOR_MSG_CHANNEL_ID = 1059592119897042984
	ROLES = [
		Role("🇫🇷","French fries"),
		Role("🇬🇧","English")
	]

	def __init__(self):
		super().__init__(command_prefix="!", intents=intents)
	
	
	async def on_ready(self):
		await self.tree.sync()
		print("Successfully synced commands")
		print(f"Logged onto {self.user}")

		guild = discord.utils.get(self.guilds)
		members = '\n - '.join([member.name for member in guild.members])
		print(f'Guild Members:\n - {members}')
		msg_channel = guild.get_channel(self.ROLE_SELECTOR_MSG_CHANNEL_ID)
		msg = None
		print("---",msg_channel)
		if msg_channel != None:
			try:
				msg = await msg_channel.fetch_message(self.ROLE_SELECTOR_MSG_ID)
			except:
				print(f"Can't retrieve message {Bot.ROLE_SELECTOR_MSG_ID}")

		if msg != None:
			for r in self.ROLES:
				await msg.add_reaction(r.emojiStr)

			for reac in msg.reactions:
				roleFound = None
				for role in self.ROLES:
					if role.emojiStr == reac.emoji:
						roleFound = await getRole(self,role.roleName)
						break
				if roleFound != None:
					async for user in reac.users():
						await giveRole(guild,user,roleFound)
		
		# print(guild.system_channel)

bot = Bot()
tcData = TCData_t()
globalCommands = ["vote"]