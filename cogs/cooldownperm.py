import discord
from discord.ext import commands

class CooldownPerm(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Add your commands here

async def setup(bot):
    await bot.add_cog(CooldownPerm(bot))
