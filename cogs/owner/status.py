import discord
import asyncio
import os

from discord.ext import commands, tasks


class Status(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        self.change_status.start() 

    @tasks.loop(seconds=10)
    async def change_status(self):
      while True:
        guilds = self.bot.guilds
        guild_count = len(guilds)

        for guild in guilds:
           member_count = sum(not member.bot for member in guild.members)

        if guild_count:
            await self.bot.change_presence(activity=discord.Game(f"auf {guild_count} Servern"), status=discord.Status.online)
            await asyncio.sleep(10)
            await self.bot.change_presence(activity=discord.Game('Python Programmierung'), status=discord.Status.online)
            await asyncio.sleep(10)
            await self.bot.change_presence(activity=discord.Game(f"mit {member_count} Usern"), status=discord.Status.online)
            await asyncio.sleep(10)


def setup(bot):
    bot.add_cog(Status(bot))