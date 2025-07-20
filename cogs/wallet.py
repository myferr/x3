import discord
from discord.ext import commands
from discord import app_commands
from data.data_manager import load_user_data

def create_fish_embed(user_data):
    embed = discord.Embed(title="Your Fish", color=discord.Color.blue())
    if not user_data["fish"]:
        embed.description = "You have no fish."
    else:
        total_value = sum(fish["value"] for fish in user_data["fish"])
        embed.description = f"You have {len(user_data['fish'])} fish with a total value of ${total_value}."
        for fish in user_data["fish"]:
            embed.add_field(name=fish['name'], value=f"Value: ${fish['value']}", inline=False)
    return embed

def create_balance_embed(user_data):
    embed = discord.Embed(title="Your Balance", color=discord.Color.green())
    embed.description = f"Your current balance is ${user_data['balance']}."
    return embed

def create_sold_fish_embed(user_data):
    embed = discord.Embed(title="Your Sold Fish", color=discord.Color.red())
    if not user_data.get("sold_fish"):
        embed.description = "You have not sold any fish."
    else:
        total_sold = len(user_data["sold_fish"])
        embed.description = f"You have sold {total_sold} fish."
        for fish in user_data["sold_fish"]:
            embed.add_field(name=fish['name'], value=f"Sold for: ${fish['value']}", inline=False)
    return embed

class WalletView(discord.ui.View):
    def __init__(self, user_id):
        super().__init__()
        self.user_id = user_id
        self.add_item(WalletDropdown(user_id))

class WalletDropdown(discord.ui.Select):
    def __init__(self, user_id):
        self.user_id = user_id
        options = [
            discord.SelectOption(label="Fish", description="View your current fish and their value."),
            discord.SelectOption(label="Balance", description="View your current balance."),
            discord.SelectOption(label="Sold Fish", description="View your sold fish."),
        ]
        super().__init__(placeholder="Choose an option...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        users = load_user_data()
        user_data = users.get(self.user_id, {"balance": 0, "fish": [], "sold_fish": []})

        if self.values[0] == "Fish":
            embed = create_fish_embed(user_data)
        elif self.values[0] == "Balance":
            embed = create_balance_embed(user_data)
        elif self.values[0] == "Sold Fish":
            embed = create_sold_fish_embed(user_data)
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

class WalletCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    wallet = app_commands.Group(name="wallet", description="Wallet commands")

    @wallet.command(name="menu", description="View your fish, balance, and sold fish.")
    async def menu(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        await interaction.response.send_message(view=WalletView(user_id), ephemeral=True)

    @wallet.command(name="fish", description="View your current fish and their value.")
    async def fish(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        users = load_user_data()
        user_data = users.get(user_id, {"balance": 0, "fish": [], "sold_fish": []})
        embed = create_fish_embed(user_data)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @wallet.command(name="balance", description="View your current balance.")
    async def balance(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        users = load_user_data()
        user_data = users.get(user_id, {"balance": 0, "fish": [], "sold_fish": []})
        embed = create_balance_embed(user_data)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @wallet.command(name="soldfish", description="View your sold fish.")
    async def soldfish(self, interaction: discord.Interaction):
        user_id = str(interaction.user.id)
        users = load_user_data()
        user_data = users.get(user_id, {"balance": 0, "fish": [], "sold_fish": []})
        embed = create_sold_fish_embed(user_data)
        await interaction.response.send_message(embed=embed, ephemeral=True)

async def setup(bot):
    await bot.add_cog(WalletCog(bot))