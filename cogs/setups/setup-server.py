import discord

from discord.ext import commands
from discord.commands import SlashCommandGroup
from utils.config import *
from datetime import datetime


class SetupServer(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    setupgroup = SlashCommandGroup("setup")
    @setupgroup.command(description="Setup the Server")
    @commands.has_permissions(administrator=True)
    async def apply(self, ctx):
        await ctx.defer()

        if commands.bot_has_permissions(administrator=True):
            await ctx.send("Setup the Serve")


def setup(bot: discord.Bot):
    bot.add_cog(SetupServer(bot))