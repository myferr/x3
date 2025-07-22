import discord
from discord.ext import commands
from discord import app_commands
from data.data_manager import save_fish_cooldown, save_operator_role, load_operator_role

class CooldownSet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="cooldown", description="Set the fish command cooldown (seconds)")
    @app_commands.describe(seconds="Cooldown in seconds (default 0.3)")
    async def cooldown(self, interaction: discord.Interaction, seconds: float = 0.3):
        guild_id = str(interaction.guild.id)
        operator_role_id = load_operator_role(guild_id)
        if operator_role_id is None:
            await interaction.response.send_message("No operator role set. Please set one with /op <role_name>.", ephemeral=True)
            return
        # Check if user has the operator role
        member = interaction.user
        if not any(role.id == operator_role_id for role in member.roles):
            await interaction.response.send_message("You do not have permission to use this command.", ephemeral=True)
            return
        save_fish_cooldown(seconds)
        await interaction.response.send_message(f"Fish command cooldown set to {seconds} seconds.", ephemeral=True)

    @app_commands.command(name="op", description="Set the operator role for cooldown command")
    @app_commands.describe(role_name="Name of the role to allow using /cooldown")
    async def op(self, interaction: discord.Interaction, role_name: str):
        if interaction.user.id != interaction.guild.owner_id:
            await interaction.response.send_message("Only the server owner can set the operator role.", ephemeral=True)
            return
        # Find the role by name
        role = discord.utils.get(interaction.guild.roles, name=role_name)
        if role is None:
            await interaction.response.send_message(f"Role '{role_name}' not found.", ephemeral=True)
            return
        save_operator_role(str(interaction.guild.id), role.id)
        await interaction.response.send_message(f"Operator role set to '{role_name}'. Members with this role can use /cooldown.", ephemeral=True)

async def setup(bot):
    await bot.add_cog(CooldownSet(bot))