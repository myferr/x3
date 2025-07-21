import discord
from discord.ext import commands
from discord import app_commands
from data.data_manager import get_or_create_user_data, save_user_data

class Equip(commands.GroupCog, name="equip"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="rod", description="Equip a fishing rod")
    @app_commands.describe(rod_name="The name of the rod to equip")
    async def equip_rod(self, interaction: discord.Interaction, rod_name: str):
        user_id = str(interaction.user.id)
        users = get_or_create_user_data(user_id)
        user_data = users[user_id]

        if rod_name not in user_data["rods"]:
            return await interaction.response.send_message("You don't own this rod.", ephemeral=True)

        user_data["equipped_rod"] = rod_name
        save_user_data(users)

        await interaction.response.send_message(f"You have equipped the {rod_name}.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Equip(bot))
