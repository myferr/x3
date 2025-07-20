
import discord
from discord.ext import commands
from discord import app_commands
from data.data_manager import load_user_data

class InventoryCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="inventory", description="View your fish inventory.")
    @app_commands.describe(page="The page of your inventory to display.")
    async def inventory(self, interaction: discord.Interaction, page: int = 1):
        user_id = str(interaction.user.id)
        users = load_user_data()

        if user_id not in users or not users[user_id]["fish"]:
            await interaction.response.send_message("Your inventory is empty. Go catch some fish! :3")
            return

        items_per_page = 10
        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page

        if page < 1:
            await interaction.response.send_message("Page number cannot be less than 1.")
            return

        user_fish = users[user_id]["fish"]
        if not user_fish:
            embed = discord.Embed(title="Inventory", description="Your inventory is empty!", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed)
            return

        embed = discord.Embed(title=f"{interaction.user.name}'s Inventory", color=discord.Color.blue())

        for i, fish in enumerate(user_fish[start_index:end_index]):
            tier = fish.get("tier", "Common")
            embed.add_field(name=f"#{start_index + i + 1} - {fish['name']} ({tier})", value=f"Weight: {fish['weight']}kg, Value: ${fish['value']}", inline=False)

        total_pages = ((len(user_fish) - 1) // items_per_page) + 1
        embed.set_footer(text=f"Page {page}/{total_pages}")
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(InventoryCog(bot))
