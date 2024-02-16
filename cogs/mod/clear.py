import discord
import asyncio

from discord.ext import commands
from discord.commands import slash_command, Option
from datetime import datetime
from utils.config import *

class ClearCommand(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @slash_command(description="clears messages in a channel")
    @commands.has_guild_permissions(manage_messages=True)
    async def clear(self, ctx,
        msgs: Option(int, "The number of messages to delete"),
        reason: Option(str, "The reason for the deletion")
    ):
        await ctx.defer()
        if commands.bot_has_guild_permissions(manage_messages=True):
            if msgs <= 0:
                em2 = discord.Embed(color=MainColor)
                file2 = discord.File("img/Error.png", filename="Error.png")
                em2.set_image(url="attachment://Error.png")

                em3 = discord.Embed(
                    title="Error",
                    description="You can't delete 0 or negative messages",
                    color=MainColor,
                    timestamp=datetime.now(),
                )
                file3 = discord.File("img/Imageline.png", filename="Imageline.png")
                em3.set_image(url="attachment://Imageline.png")
                em3.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
                em3.set_thumbnail(url=self.bot.user.avatar.url)

                await ctx.respond(embeds=[em2, em3], files=[file2, file3], ephemeral=True)
                return
            
            else:
                async for message in ctx.channel.history(limit=msgs):
                    await message.delete()

                em0 = discord.Embed(color=MainColor)
                file0 = discord.File("img/Delete.png", filename="Delete.png")
                em0.set_image(url="attachment://Delete.png")

                em1 = discord.Embed(
                    title="Messages Deleted",
                    color=MainColor,
                    timestamp=datetime.now(),
                )
                em1.add_field(name="Moderator", value=f"{ctx.author.mention} | `{ctx.author.id}`", inline=False)
                em1.add_field(name="Reason", value=reason, inline=False)
                em1.add_field(name="Messages Deleted", value=msgs, inline=False)
                file1 = discord.File("img/Imageline.png", filename="Imageline.png")
                em1.set_image(url="attachment://Imageline.png")
                em1.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
                em1.set_thumbnail(url=self.bot.user.avatar.url)

                msg = await ctx.send(embeds=[em0, em1], files=[file0, file1])
                await asyncio.sleep(10)
                await msg.delete()

        else:
            em4 = discord.Embed(color=MainColor)
            file4 = discord.File("img/Error.png", filename="Error.png")
            em4.set_image(url="attachment://Error.png")

            em5 = discord.Embed(
                title="Error",
                description="I don't have the permission to delete messages",
                color=MainColor,
                timestamp=datetime.now(),
            )
            file5 = discord.File("img/Imageline.png", filename="Imageline.png")
            em5.set_image(url="attachment://Imageline.png")
            em5.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            em5.set_thumbnail(url=self.bot.user.avatar.url)

            await ctx.respond(embeds=[em4, em5], files=[file4, file5], ephemeral=True)
            return

def setup(bot: discord.Bot):
    bot.add_cog(ClearCommand(bot))
