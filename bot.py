
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
from data.data_manager import setup_data_files

load_dotenv()
TOKEN = os.getenv("TOKEN")

setup_data_files()

intents = discord.Intents.default()

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.change_presence(activity=discord.Game(name="with a fishing rod"))

async def setup_hook():
    for filename in os.listdir("./cogs"):
        if filename.endswith(".py"):
            await bot.load_extension(f"cogs.{filename[:-3]}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)

bot.setup_hook = setup_hook

bot.run(TOKEN)
