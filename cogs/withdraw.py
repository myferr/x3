import discord
from discord.ext import commands
from discord import app_commands
from data.data_manager import get_or_create_user_data, save_user_data

class Withdraw(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="withdraw", description="Withdraw money from your bank.")
    @app_commands.describe(amount="The amount to withdraw.")
    async def withdraw(self, interaction: discord.Interaction, amount: int):
        if amount <= 0:
            return await interaction.response.send_message("You must withdraw a positive amount.", ephemeral=True)

        user = interaction.user
        user_id = str(user.id)
        users = get_or_create_user_data(user_id)
        data = users[user_id]

        if data.get("deposit", 0) < amount:
            return await interaction.response.send_message("You don't have enough money in your bank to withdraw.", ephemeral=True)

        data["deposit"] -= amount
        data["balance"] = data.get("balance", 0) + amount
        users[user_id] = data
        save_user_data(users)

        await interaction.response.send_message(f"You have withdrawn ${amount} from your bank.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Withdraw(bot))