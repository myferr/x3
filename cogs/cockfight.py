import discord
from discord.ext import commands
from discord import app_commands
import os
import json
import random

DATA_DIR = "data"
USER_DATA_FILE = os.path.join(DATA_DIR, "users.json")

def load_user_data():
    if not os.path.exists(USER_DATA_FILE):
        return {}
    if os.stat(USER_DATA_FILE).st_size == 0:
        return {}
    with open(USER_DATA_FILE, "r") as f:
        return json.load(f)

def save_user_data(data):
    with open(USER_DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

class Cockfight(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="cockfight", description="Gamble your balance in a 50/50 fight! Win double or lose it all.")
    @app_commands.describe(amount="Amount of money to bet, or type 'all'")
    async def cockfight(self, interaction: discord.Interaction, amount: str):
        user_id = str(interaction.user.id)
        users = load_user_data()

        if user_id not in users:
            users[user_id] = {
                "balance": 0,
                "fish": [],
                "sold_fish": [],
                "bait": {"worm": 0, "magic_bait": 0},
                "rods": [],
                "equipped_rod": None
            }

        balance = users[user_id]["balance"]

        # Parse "all" or int
        if amount.lower() == "all":
            if balance <= 0:
                await interaction.response.send_message("You have no money to gamble.", ephemeral=True)
                return
            bet = balance
        else:
            try:
                bet = int(amount)
            except ValueError:
                await interaction.response.send_message("Invalid amount. Enter a number or use 'all'.", ephemeral=True)
                return
            if bet <= 0:
                await interaction.response.send_message("Bet must be greater than 0.", ephemeral=True)
                return
            if bet > balance:
                await interaction.response.send_message("You don't have enough money to bet that much.", ephemeral=True)
                return

        # 50% chance to win
        win = random.random() < 0.5

        if win:
            users[user_id]["balance"] += bet
            embed = discord.Embed(
                title="Cockfight Victory!",
                description=f"You won the cockfight and earned **${bet * 2}**!",
                color=discord.Color.green()
            )
        else:
            users[user_id]["balance"] -= bet
            embed = discord.Embed(
                title="Cockfight Defeat...",
                description=f"Your chicken lost the fight. You lost **${bet}**.",
                color=discord.Color.red()
            )

        save_user_data(users)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Cockfight(bot))

