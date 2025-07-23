import discord
from discord.ext import commands
from discord import app_commands
from data.data_manager import get_or_create_user_data, save_user_data

class Deposit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="deposit", description="Deposit money into your bank.")
    @app_commands.describe(amount="The amount to deposit.")
    async def deposit(self, interaction: discord.Interaction, amount: int):
        if amount <= 0:
            return await interaction.response.send_message("You must deposit a positive amount.", ephemeral=True)

        user = interaction.user
        user_id = str(user.id)
        users = get_or_create_user_data(user_id)
        data = users[user_id]

        if data["balance"] < amount:
            return await interaction.response.send_message("You don't have enough money to deposit.", ephemeral=True)

        data["balance"] -= amount
        data["deposit"] = data.get("deposit", 0) + amount
        users[user_id] = data
        save_user_data(users)

        await interaction.response.send_message(f"You have deposited ${amount} into your bank.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Deposit(bot))