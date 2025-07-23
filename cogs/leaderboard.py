
import discord
from discord.ext import commands
from discord import app_commands, ui
from data.data_manager import load_user_data

class LeaderboardView(ui.View):
    def __init__(self, bot, interaction, sorted_users, leaderboard_type):
        super().__init__(timeout=180)
        self.bot = bot
        self.interaction = interaction
        self.sorted_users = sorted_users
        self.leaderboard_type = leaderboard_type
        self.current_page = 1
        self.items_per_page = 5
        self.total_pages = ((len(self.sorted_users) - 1) // self.items_per_page) + 1

    async def update_embed(self):
        start_index = (self.current_page - 1) * self.items_per_page
        end_index = start_index + self.items_per_page

        if self.leaderboard_type == "balance":
            embed = discord.Embed(title="Leaderboard - Balance", color=discord.Color.gold())
            for i, (user_id, data) in enumerate(self.sorted_users[start_index:end_index]):
                try:
                    user = await self.bot.fetch_user(int(user_id))
                    balance = data.get('balance', 0)
                    deposit = data.get('deposit', 0)
                    embed.add_field(name=f"#{start_index + i + 1} - {user.name}", value=f"Wallet: ${balance} | Bank: ${deposit}", inline=False)
                except discord.NotFound:
                    balance = data.get('balance', 0)
                    deposit = data.get('deposit', 0)
                    embed.add_field(name=f"#{start_index + i + 1} - *Unknown User*", value=f"Wallet: ${balance} | Bank: ${deposit}", inline=False)
        else:
            embed = discord.Embed(title="Leaderboard - Fish", color=discord.Color.blue())
            for i, (user_id, data) in enumerate(self.sorted_users[start_index:end_index]):
                try:
                    user = await self.bot.fetch_user(int(user_id))
                    fish_count = len(data.get('fish', []))
                    embed.add_field(name=f"#{start_index + i + 1} - {user.name}", value=f"{fish_count} fish", inline=False)
                except discord.NotFound:
                    fish_count = len(data.get('fish', []))
                    embed.add_field(name=f"#{start_index + i + 1} - *Unknown User*", value=f"{fish_count} fish", inline=False)
        
        self.previous_button.disabled = self.current_page == 1
        self.next_button.disabled = self.current_page == self.total_pages

        embed.set_footer(text=f"Page {self.current_page}/{self.total_pages}")
        return embed

    @ui.button(label="Previous", style=discord.ButtonStyle.grey)
    async def previous_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer()
        if self.current_page > 1:
            self.current_page -= 1
            embed = await self.update_embed()
            await interaction.edit_original_response(embed=embed, view=self)

    @ui.button(label="Next", style=discord.ButtonStyle.grey)
    async def next_button(self, interaction: discord.Interaction, button: ui.Button):
        await interaction.response.defer()
        if self.current_page < self.total_pages:
            self.current_page += 1
            embed = await self.update_embed()
            await interaction.edit_original_response(embed=embed, view=self)

class LeaderboardCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    leaderboard = app_commands.Group(name="leaderboard", description="Display the server leaderboard.")

    @leaderboard.command(name="balance", description="Display the server leaderboard by balance.")
    async def balance(self, interaction: discord.Interaction):
        users = load_user_data()
        sorted_users = sorted(users.items(), key=lambda item: item[1].get("balance", 0) + item[1].get("deposit", 0), reverse=True)

        if not sorted_users:
            embed = discord.Embed(title="Leaderboard - Balance", description="The leaderboard is empty!", color=discord.Color.gold())
            await interaction.response.send_message(embed=embed)
            return

        view = LeaderboardView(self.bot, interaction, sorted_users, "balance")
        embed = await view.update_embed()
        await interaction.response.send_message(embed=embed, view=view)

    @leaderboard.command(name="fish", description="Display the server leaderboard by fish caught.")
    async def fish(self, interaction: discord.Interaction):
        users = load_user_data()
        sorted_users = sorted(users.items(), key=lambda item: len(item[1].get("fish", [])), reverse=True)

        if not sorted_users:
            embed = discord.Embed(title="Leaderboard - Fish", description="The leaderboard is empty!", color=discord.Color.blue())
            await interaction.response.send_message(embed=embed)
            return

        view = LeaderboardView(self.bot, interaction, sorted_users, "fish")
        embed = await view.update_embed()
        await interaction.response.send_message(embed=embed, view=view)

async def setup(bot):
    await bot.add_cog(LeaderboardCog(bot))
