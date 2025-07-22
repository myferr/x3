import discord
from discord.ext import commands

class CooldownPerm(commands.Cog):
    """
    Command for handling permission-related commands for cooldown features.
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="permtest", help="Test if the cog is loaded and working.")
    async def permtest(self, ctx):
        await ctx.send("CooldownPerm cog is loaded and responding!")

async def setup(bot):
    await bot.add_cog(CooldownPerm(bot))
