import discord
from discord.ext import commands
from discord import app_commands
import os
import json

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

class Gift(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="gift", description="Gift another user some of your money.")
    @app_commands.describe(user="The user you want to gift money to", amount="The amount of money to gift")
    async def gift(self, interaction: discord.Interaction, user: discord.User, amount: int):
        sender_id = str(interaction.user.id)
        receiver_id = str(user.id)

        if user.id == interaction.user.id:
            await interaction.response.send_message("You can't gift yourself!", ephemeral=True)
            return

        if amount <= 0:
            await interaction.response.send_message("Gift amount must be greater than 0.", ephemeral=True)
            return

        users = load_user_data()

        # Ensure both users exist
        if sender_id not in users:
            users[sender_id] = {
                "balance": 0,
                "fish": [],
                "sold_fish": [],
                "bait": {"worm": 0, "magic_bait": 0},
                "rods": [],
                "equipped_rod": None
            }
        if receiver_id not in users:
            users[receiver_id] = {
                "balance": 0,
                "fish": [],
                "sold_fish": [],
                "bait": {"worm": 0, "magic_bait": 0},
                "rods": [],
                "equipped_rod": None
            }

        if users[sender_id]["balance"] < amount:
            await interaction.response.send_message("You don't have enough money to gift that much.", ephemeral=True)
            return

        # Perform the gift
        users[sender_id]["balance"] -= amount
        users[receiver_id]["balance"] += amount
        save_user_data(users)

        embed = discord.Embed(
            title="🎁 Gift Successful!",
            description=f"{interaction.user.mention} gifted **${amount}** to {user.mention}!",
            color=discord.Color.gold()
        )
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(Gift(bot))

