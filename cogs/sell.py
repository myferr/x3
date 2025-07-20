import discord
from discord.ext import commands
from discord import app_commands
from data.data_manager import load_user_data, save_user_data

class SellCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    sell = app_commands.Group(name="sell", description="Sell your fish.")

    @sell.command(name="some", description="Sell a specific number of fish.")
    @app_commands.describe(amount="The number of fish to sell.")
    async def some(self, interaction: discord.Interaction, amount: int):
        user_id = str(interaction.user.id)
        users = load_user_data()

        if user_id not in users or not users[user_id]["fish"]:
            await interaction.response.send_message("You have no fish to sell! you should probably go catch some 3:")
            return

        if amount <= 0:
            await interaction.response.send_message("Please provide a positive number. 3:")
            return

        if amount > len(users[user_id]["fish"]):
            await interaction.response.send_message(f"You only have {len(users[user_id]['fish'])} fish to sell. =3")
            return

        sold_fish = users[user_id]["fish"][:amount]
        total_value = sum(fish["value"] for fish in sold_fish)

        tier_counts = {}
        for fish in sold_fish:
            tier = fish.get("tier", "Common")
            tier_counts[tier] = tier_counts.get(tier, 0) + 1

        users[user_id].setdefault("sold_fish", []).extend(sold_fish)
        users[user_id]["fish"] = users[user_id]["fish"][amount:]
        users[user_id]["balance"] += total_value
        save_user_data(users)

        response = f"You sold {amount} fish for ${total_value}.\n\n**Breakdown:**\n"
        for tier, count in sorted(tier_counts.items()):
            response += f"- {tier}: {count}\n"

        await interaction.response.send_message(response)

    @sell.command(name="all", description="Sell all your fish.")
    async def all(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        users = load_user_data()

        if user_id not in users or not users[user_id]["fish"]:
            await interaction.response.send_message("You have no fish to sell! you should probably go catch some 3:")
            return

        sold_fish = users[user_id]["fish"]
        total_value = sum(fish["value"] for fish in sold_fish)

        tier_counts = {}
        for fish in sold_fish:
            tier = fish.get("tier", "Common")
            tier_counts[tier] = tier_counts.get(tier, 0) + 1

        users[user_id].setdefault("sold_fish", []).extend(sold_fish)
        users[user_id]["fish"] = []
        users[user_id]["balance"] += total_value
        save_user_data(users)

        response = f"You sold all your fish for ${total_value}! x3\n\n**Breakdown:**\n"
        for tier, count in sorted(tier_counts.items()):
            response += f"- {tier}: {count}\n"

        await interaction.response.send_message(response)

async def setup(bot):
    await bot.add_cog(SellCog(bot))
