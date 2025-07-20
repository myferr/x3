
import discord
from discord.ext import commands
from discord import app_commands

class TiersCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="tiers", description="View the fish tiers and their catch rates.")
    async def tiers(self, interaction: discord.Interaction):
        fish_tiers = {
            "Common": {"color": discord.Color.blue(), "chance": 0.7},
            "Uncommon": {"color": discord.Color.green(), "chance": 0.2},
            "Rare": {"color": discord.Color.gold(), "chance": 0.08},
            "Legendary": {"color": discord.Color.purple(), "chance": 0.02}
        }

        embed = discord.Embed(title="Fish Tiers", color=discord.Color.orange())

        for tier, data in fish_tiers.items():
            chance = data['chance'] * 100
            embed.add_field(name=tier, value=f"Catch Rate: {chance:.1f}%", inline=False)

        await interaction.response.send_message(embed=embed)

async def setup(bot):
    await bot.add_cog(TiersCog(bot))
