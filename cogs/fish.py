
import discord
from discord.ext import commands
import random
from data.data_manager import load_user_data, save_user_data

from discord import app_commands

class FishCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="fish", description="Catch a fish!")
    async def fish(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        users = load_user_data()

        if user_id not in users:
            users[user_id] = {"balance": 0, "fish": []}

        fish_types = ["Salmon", "Tuna", "Cod", "Trout", "Sardine"]
        fish_name = random.choice(fish_types)
        fish_weight = round(random.uniform(0.1, 10.0), 2)
        fish_value = int(fish_weight * 5)  # Value is 5 times the weight

        users[user_id]["fish"].append({"name": fish_name, "weight": fish_weight, "value": fish_value})
        save_user_data(users)

        embed = discord.Embed(title="You caught a fish! :3", color=discord.Color.blue())
        embed.add_field(name="Fish", value=fish_name, inline=True)
        embed.add_field(name="Weight", value=f"{fish_weight}kg", inline=True)
        embed.add_field(name="Value", value=f"${fish_value}", inline=True)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(FishCog(bot))
