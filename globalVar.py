import discord
from discord import app_commands
from discord.ext import commands

intents = discord.Intents.all()

class Bot(commands.Bot):

    ALLOWED_CHANNELS = ["bot-mania"]

    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)
    
    async def on_ready(self):
        await self.tree.sync()
        print("Successfully synced commands")
        print(f"Logged onto {self.user}")

bot = Bot()