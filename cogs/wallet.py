import discord
from discord.ext import commands
from discord import app_commands
from data.data_manager import load_user_data

class CardCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="wallet", description="View a user's profile wallet.")
    @app_commands.describe(user="The user to view the wallet card.")
    async def card(self, interaction: discord.Interaction, user: discord.User):
        users = load_user_data()
        user_id = str(user.id)
        user_data = users.get(user_id, {"balance": 0, "fish": [], "sold_fish": []})

        fish_count = len(user_data.get("fish", []))
        inventory_worth = sum(fish.get("value", 0) for fish in user_data.get("fish", []))
        balance = user_data.get("balance", 0)
        sold_count = len(user_data.get("sold_fish", []))

        embed = discord.Embed(
            title=f"{user.name}'s Profile Wallet :3",
            color=discord.Color.purple(),
            description=f"**Balance:** ${balance}\n"
                        f"**Fish in Inventory:** {fish_count}\n"
                        f"**Inventory Worth:** ${inventory_worth}\n"
                        f"**Sold Fish:** {sold_count}"
        )
        embed.set_thumbnail(url=user.display_avatar.url)
        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(CardCog(bot))
