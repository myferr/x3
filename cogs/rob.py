import discord
from discord.ext import commands
from discord import app_commands
import time
import random
import os
import json

DATA_DIR = "data"
ROB_COOLDOWN_FILE = os.path.join(DATA_DIR, "rob_cooldowns.json")
USER_DATA_FILE = os.path.join(DATA_DIR, "users.json")

def load_rob_cooldowns():
    if not os.path.exists(ROB_COOLDOWN_FILE):
        return {}
    if os.stat(ROB_COOLDOWN_FILE).st_size == 0:
        return {}
    with open(ROB_COOLDOWN_FILE, "r") as f:
        return json.load(f)

def save_rob_cooldowns(data):
    with open(ROB_COOLDOWN_FILE, "w") as f:
        json.dump(data, f, indent=4)

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

class RobCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.cooldown_time = 3600  # 1 hour in seconds

    @app_commands.command(name="rob", description="Try to rob someone's balance!")
    @app_commands.describe(target="The user to rob")
    async def rob(self, interaction: discord.Interaction, target: discord.User):
        robber_id = str(interaction.user.id)
        target_id = str(target.id)

        if robber_id == target_id:
            await interaction.response.send_message("You cannot rob yourself!", ephemeral=True)
            return

        now = time.time()
        rob_cooldowns = load_rob_cooldowns()
        users = load_user_data()

        if robber_id not in users:
            users[robber_id] = {"balance": 0, "fish": [], "sold_fish": [], "bait": {"worm": 0, "magic_bait": 0}, "rods": [], "equipped_rod": None}
        if target_id not in users:
            users[target_id] = {"balance": 0, "fish": [], "sold_fish": [], "bait": {"worm": 0, "magic_bait": 0}, "rods": [], "equipped_rod": None}

        last_rob_time = rob_cooldowns.get(robber_id, 0)
        time_since_last_rob = now - last_rob_time
        if time_since_last_rob < self.cooldown_time:
            remaining = round((self.cooldown_time - time_since_last_rob) / 60, 1)
            embed = discord.Embed(
                title="Cooldown Active",
                description=f"You are on cooldown! Try robbing again in {remaining} minutes.",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        target_balance = users[target_id].get("balance", 0)
        if target_balance <= 0:
            embed = discord.Embed(
                title="No Balance",
                description="This person has no balance, try again!",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            return

        robber_balance = users[robber_id].get("balance", 0)

        max_rob_amount = int(target_balance / 1.3)
        max_rob_amount = max(max_rob_amount, 1)

        max_lose_amount = int(robber_balance / 1.3)
        max_lose_amount = max(max_lose_amount, 0)

        success_chance = 0.55
        success = random.random() < success_chance

        rob_cooldowns[robber_id] = now
        save_rob_cooldowns(rob_cooldowns)

        if success:
            stolen_amount = random.randint(1, max_rob_amount)
            users[target_id]["balance"] -= stolen_amount
            users[robber_id]["balance"] += stolen_amount
            save_user_data(users)

            embed = discord.Embed(
                title="Robbery Successful!",
                description=f"You successfully robbed {target.mention} and stole **${stolen_amount}**!",
                color=discord.Color.green()
            )
            await interaction.response.send_message(embed=embed)
        else:
            lost_amount = random.randint(1, max_lose_amount) if max_lose_amount > 0 else 0
            users[robber_id]["balance"] -= lost_amount
            if users[robber_id]["balance"] < 0:
                users[robber_id]["balance"] = 0
            save_user_data(users)

            embed = discord.Embed(
                title="Robbery Failed!",
                description=f"You tried to rob {target.mention} but got caught! You lost **${lost_amount}**.",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(RobCog(bot))
