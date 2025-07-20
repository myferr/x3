
import discord
from discord.ext import commands
import random
import time # Import time for cooldowns
from data.data_manager import load_user_data, save_user_data, load_cooldown_data, save_cooldown_data

from discord import app_commands

class FishCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="fish", description="Catch a fish!")
    async def fish(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        current_time = time.time()
        cooldown_time = 3 # seconds

        cooldowns = load_cooldown_data()

        if user_id in cooldowns and current_time - cooldowns[user_id] < cooldown_time:
            remaining_time = round(cooldown_time - (current_time - cooldowns[user_id]), 1)
            await interaction.response.send_message(f"You're on cooldown! Please wait {remaining_time} seconds before fishing again.", ephemeral=True)
            return

        cooldowns[user_id] = current_time
        save_cooldown_data(cooldowns)

        users = load_user_data()

        # Ensure user data structure is correct
        if user_id not in users or not isinstance(users[user_id], dict) or "fish" not in users[user_id] or "balance" not in users[user_id]:
            users[user_id] = {"balance": 0, "fish": []}

        

        fish_types = [
            "Salmon", "Tuna", "Cod", "Trout", "Sardine", "Bass", "Pike", "Carp", 
            "Catfish", "Sturgeon", "Eel", "Megalodon", "Coelacanth", "Oarfish",
            "Blobfish", "Anglerfish", "Pufferfish", "Lionfish", "Swordfish", "Marlin",
            "Clownfish", "Seahorse", "Manta Ray", "Sunfish"
        ]

        fish_tiers = {
            "Common": {"color": discord.Color.blue(), "chance": 0.7},
            "Uncommon": {"color": discord.Color.green(), "chance": 0.2},
            "Rare": {"color": discord.Color.gold(), "chance": 0.08},
            "Legendary": {"color": discord.Color.purple(), "chance": 0.02}
        }

        tier_choice = random.choices(list(fish_tiers.keys()), weights=[tier["chance"] for tier in fish_tiers.values()], k=1)[0]
        
        chosen_tier = fish_tiers[tier_choice]
        fish_name = random.choice(fish_types)
        fish_weight = round(random.uniform(0.1, 10.0), 2)
        fish_value = int(fish_weight * 5 * (list(fish_tiers.keys()).index(tier_choice) + 1))

        users[user_id]["fish"].append({"name": fish_name, "weight": fish_weight, "value": fish_value, "tier": tier_choice})
        save_user_data(users)

        embed = discord.Embed(title=f"You caught a {tier_choice} fish! :3", color=chosen_tier["color"])
        embed.add_field(name="Fish", value=fish_name, inline=True)
        embed.add_field(name="Weight", value=f"{fish_weight}kg", inline=True)
        embed.add_field(name="Value", value=f"${fish_value}", inline=True)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(FishCog(bot))
