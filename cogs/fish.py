
import discord
from discord.ext import commands
import random
import time # Import time for cooldowns
from data.data_manager import load_user_data, save_user_data, load_cooldown_data, save_cooldown_data, get_or_create_user_data

from discord import app_commands

class FishCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="fish", description="Catch a fish!")
    @app_commands.describe(bait_type="The type of bait to use")
    @app_commands.choices(bait_type=[
        app_commands.Choice(name="worm", value="worm"),
        app_commands.Choice(name="magic_bait", value="magic_bait"),
    ])
    async def fish(self, interaction: discord.Interaction, bait_type: str = None):
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

        users = get_or_create_user_data(user_id)
        user_data = users[user_id]

        bait_message = ""
        rod_rarity_multiplier = 1.0
        rod_weight_multiplier = 1.0
        equipped_rod = user_data.get("equipped_rod")

        if equipped_rod == "basic_rod":
            rod_rarity_multiplier = 1.15
        elif equipped_rod == "golden_rod":
            rod_rarity_multiplier = 1.25
            rod_weight_multiplier = 1.15

        rarity_multiplier *= rod_rarity_multiplier
        weight_multiplier *= rod_weight_multiplier

        if bait_type:
            if user_data["bait"].get(bait_type, 0) > 0:
                user_data["bait"][bait_type] -= 1
                bait_message = f"Used 1 {bait_type}."
                if bait_type == "magic_bait":
                    rarity_multiplier = 1.25
                    weight_multiplier = 1.25
                elif bait_type == "worm":
                    weight_multiplier = 1.15
                save_user_data(users)
            else:
                await interaction.response.send_message(f"You don't have any {bait_type}.", ephemeral=True)
                return

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

        chances = [tier["chance"] for tier in fish_tiers.values()]
        if rarity_multiplier > 1.0:
            chances = [chance * rarity_multiplier if tier != "Common" else chance for tier, chance in zip(fish_tiers.keys(), chances)]
        
        total_chance = sum(chances)
        chances = [chance / total_chance for chance in chances]

        tier_choice = random.choices(list(fish_tiers.keys()), weights=chances, k=1)[0]
        
        chosen_tier = fish_tiers[tier_choice]
        fish_name = random.choice(fish_types)
        fish_weight = round(random.uniform(0.1, 10.0) * weight_multiplier, 2)
        fish_value = int(fish_weight * 5 * (list(fish_tiers.keys()).index(tier_choice) + 1))

        user_data["fish"].append({"name": fish_name, "weight": fish_weight, "value": fish_value, "tier": tier_choice})
        users[user_id] = user_data
        save_user_data(users)

        embed = discord.Embed(title=f"You caught a {tier_choice} fish! :3", color=chosen_tier["color"])
        embed.add_field(name="Fish", value=fish_name, inline=True)
        embed.add_field(name="Weight", value=f"{fish_weight}kg", inline=True)
        embed.add_field(name="Value", value=f"${fish_value}", inline=True)
        await interaction.response.send_message(embed=embed, content=bait_message)

async def setup(bot):
    await bot.add_cog(FishCog(bot))
