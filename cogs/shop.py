import discord
from discord.ext import commands
from discord import app_commands

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="shop", description="Browse the fishing shop")
    async def shop(self, interaction: discord.Interaction):
        options = [
            discord.SelectOption(label="Fishing Rods", value="rod"),
            discord.SelectOption(label="Bait", value="bait")
        ]

        view = ShopView(interaction.user)
        view.add_item(CategorySelect(options, interaction.user))

        embed = discord.Embed(title="🎣 Fishing Shop", description="Choose a category to shop from.", color=discord.Color.green())
        await interaction.response.send_message(embed=embed, view=view)

class CategorySelect(discord.ui.Select):
    def __init__(self, options, user):
        super().__init__(placeholder="Select a category...", options=options)
        self.user = user

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.user:
            return await interaction.response.send_message("You're not allowed to use this menu.", ephemeral=True)

        view = ShopView(self.user)
        if self.values[0] == "rod":
            embed = discord.Embed(title="🪝 Fishing Rods", description="Buy better rods to catch rarer fish!", color=discord.Color.blurple())
            embed.add_field(name="Basic Rod", value="$500 - Slightly increases rarity", inline=False)
            embed.add_field(name="Golden Rod", value="$1500 - Greatly increases rarity and weight", inline=False)
        else:
            embed = discord.Embed(title="🪱 Bait", description="Buy bait to increase fish value. Bait is consumed each use.", color=discord.Color.gold())
            embed.add_field(name="Worm", value="$100 - Slightly boosts fish weight", inline=False)
            embed.add_field(name="Magic Bait", value="$350 - Boosts fish weight and rarity", inline=False)

        select = BuySelect(self.values[0], self.user)
        view.add_item(select)
        await interaction.response.edit_message(embed=embed, view=view)

class BuySelect(discord.ui.Select):
    def __init__(self, category, user):
        self.category = category
        self.user = user

        options = []
        if category == "bait":
            options = [
                discord.SelectOption(label="Worm", value="worm"),
                discord.SelectOption(label="Magic Bait", value="magic_bait")
            ]
        else:
            options = [
                discord.SelectOption(label="Basic Rod", value="basic_rod"),
                discord.SelectOption(label="Golden Rod", value="golden_rod")
            ]

        super().__init__(placeholder=f"Buy {category.title()}...", options=options)

    async def callback(self, interaction: discord.Interaction):
        if interaction.user != self.user:
            return await interaction.response.send_message("You're not allowed to use this menu.", ephemeral=True)

        await interaction.response.send_message(f"Use `/buy {self.category} {self.values[0]}` to buy!", ephemeral=True)

class ShopView(discord.ui.View):
    def __init__(self, user):
        super().__init__(timeout=60)
        self.user = user

async def setup(bot):
    await bot.add_cog(Shop(bot))

