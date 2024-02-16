import discord

from discord.ext import commands
from discord.commands import slash_command, Option
from utils.config import *
from datetime import datetime


class KickCommand(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command(description="kicks a member from the server")
    async def kick(self, ctx, member: Option(discord.Member, "The member to kick"), reason: Option(str, "The reason for the kick")):
        await ctx.respond(f"Hey {ctx.author.mention}")


def setup(bot: discord.Bot):
    bot.add_cog(KickCommand(bot))