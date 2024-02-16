import discord

from discord.ext import commands
from discord.commands import slash_command
from utils.config import *
from datetime import datetime


class RulesPy(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command(description="hello")
    async def rules(self, ctx, channel: discord.TextChannel = None):
        channel_id = channel.id
        channel = self.bot.get_channel(channel_id)

        em0 = discord.Embed(color=MainColor)
        file0 = discord.File('img/Rules.png', filename='Rules.png')
        em0.set_image(url="attachment://Rules.png")

        em1 = discord.Embed(
            title="Rules",
            description="Please read the rules before you start chatting.",
            color=MainColor,
            timestamp=datetime.now()
        )
        em1.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
        em1.set_thumbnail(url=self.bot.user.avatar.url)
        file1 = discord.File('img/Imageline.png', filename='Imageline.png')
        em1.set_image(url="attachment://Imageline.png")

        await channel.send(embeds=[em0, em1], files=[file0, file1])
        await ctx.respond("Rules sent to " + channel.mention, ephemeral=True)


def setup(bot: discord.Bot):
    bot.add_cog(RulesPy(bot))