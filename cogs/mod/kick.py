import discord

from discord.ext import commands
from discord.commands import slash_command, Option
from utils.config import *
from datetime import datetime


class KickCommand(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command(description="kicks a member from the server")
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: Option(discord.Member, "The member to kick"), reason: Option(str, "The reason for the kick")):
        
        if commands.bot_has_guild_permissions(kick_members=True):
            await member.kick(reason=reason)
            em0 = discord.Embed(color=MainColor)
            file0 = discord.File("img/Kick.png", filename="Kick.png")
            em0.set_image(url="attachment://Kick.png")

            em1 = discord.Embed(
                title="Member Kicked",
                color=MainColor,
                timestamp=datetime.now(),
            )
            em1.add_field(name="Moderator", value=f"{ctx.author.mention} | `{ctx.author.id}`", inline=False)
            em1.add_field(name="Reason", value=reason, inline=False)
            em1.add_field(name="Member Kicked", value=f"{member.mention} | `{member.id}`", inline=False)
            file1 = discord.File("img/Imageline.png", filename="Imageline.png")
            em1.set_image(url="attachment://Imageline.png")
            em1.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            em1.set_thumbnail(url=self.bot.user.avatar.url)

            await ctx.respond(embeds=[em0, em1], files=[file0, file1])


def setup(bot: discord.Bot):
    bot.add_cog(KickCommand(bot))