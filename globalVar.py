import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.all()

class Role:
	def __init__(self,emojiStr:str,roleName:str) -> None:
		self.emojiStr = emojiStr
		self.roleName = roleName

class Bot(commands.Bot):

	ALLOWED_CHANNELS = ["bot-mania"]
	ROLE_SELECTOR_MSG_ID = 1059592418875420690
	ROLE_SELECTOR_MSG_CHANNEL_ID = 1059592119897042984
	ROLES = [
		Role("🇫🇷","French fries")
	]

	def __init__(self):
		super().__init__(command_prefix="!", intents=intents)
	
	async def on_ready(self):
		await self.tree.sync()
		print("Successfully synced commands")
		print(f"Logged onto {self.user}")

		guild = discord.utils.get(bot.guilds)
		msg_channel = bot.get_channel(self.ROLE_SELECTOR_MSG_CHANNEL_ID)
		msg = await msg_channel.fetch_message(self.ROLE_SELECTOR_MSG_ID)
		
		for r in self.ROLES:
			await msg.add_reaction(r.emojiStr)

bot = Bot()