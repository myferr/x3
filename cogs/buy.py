import discord
from discord.ext import commands
from discord import app_commands
from data.data_manager import load_user_data, save_user_data, get_or_create_user_data

class Buy(commands.GroupCog, name="buy"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="bait", description="Buy bait")
    @app_commands.describe(name="Name of the bait to buy", amount="Amount of bait")
    async def buy_bait(self, interaction: discord.Interaction, name: str, amount: int = 1):
        bait_prices = {"worm": 100, "magic_bait": 350}
        if name not in bait_prices:
            return await interaction.response.send_message("Unknown bait type.", ephemeral=True)

        user = interaction.user
        user_id = str(user.id)
        users = get_or_create_user_data(user_id)
        data = users[user_id]
        total_cost = bait_prices[name] * amount

        if data["balance"] < total_cost:
            return await interaction.response.send_message("You can't afford this bait.", ephemeral=True)

        data["balance"] -= total_cost
        data["bait"][name] = data["bait"].get(name, 0) + amount
        users[user_id] = data
        save_user_data(users)

        await interaction.response.send_message(f"You bought {amount}x {name} for ${total_cost}!", ephemeral=True)

    @app_commands.command(name="rod", description="Buy a fishing rod")
    @app_commands.describe(name="Name of the rod to buy")
    async def buy_rod(self, interaction: discord.Interaction, name: str):
        rod_prices = {"basic_rod": 500, "golden_rod": 1500}
        if name not in rod_prices:
            return await interaction.response.send_message("Unknown rod type.", ephemeral=True)

        user = interaction.user
        user_id = str(user.id)
        users = get_or_create_user_data(user_id)
        data = users[user_id]

        if name in data["rods"]:
            return await interaction.response.send_message("You already own this rod.", ephemeral=True)

        if data["balance"] < rod_prices[name]:
            return await interaction.response.send_message("You can't afford this rod.", ephemeral=True)

        data["balance"] -= rod_prices[name]
        data["rods"].append(name)
        users[user_id] = data
        save_user_data(users)

        await interaction.response.send_message(f"You bought a {name}!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Buy(bot))

