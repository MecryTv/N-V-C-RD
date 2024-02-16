import discord
import os
import aiosqlite

from discord.ext import commands
from discord.commands import slash_command
from utils.config import *
from datetime import datetime


class JoinNewGuild(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect("data/newguilds.db") as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS guilds (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    guild_id INTEGER,
                    guild_name TEXT,
                    guild_owner TEXT,
                    guild_owner_id INTEGER,
                    guild_members INTEGER
                )    
            ''')
            await db.commit()

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        guild_id = int(os.getenv('DEV_SERVER_ID'))
        dev_guild = self.bot.get_guild(guild_id)
        owner = dev_guild.owner

        member_count = sum(not member.bot for member in guild.members)

        async with aiosqlite.connect("data/newguilds.db") as db:
            await db.execute('''
                INSERT INTO guilds (guild_id, guild_name, guild_owner, guild_owner_id, guild_members)
                VALUES (?, ?, ?, ?, ?)
            ''', (guild_id, guild.name, guild.owner.name, guild.owner.id, member_count))
            await db.commit()  

        em0 = discord.Embed(color=MainColor)
        file1 = discord.File("img/Guild.png", filename="Guild.png")
        em0.set_image(url="attachment://Guild.png")

        em1 = discord.Embed(
            title="Discord Server",
            description=f"Der Bot ist einem neuen Server beigetreten.",
            color=MainColor,
            timestamp=datetime.now()
        )
        em1.add_field(name="Server Name", value=f"{guild.name}", inline=False)
        em1.add_field(name="Server ID", value=f"```{guild.id}```", inline=False)
        em1.add_field(name="Server Besitzer", value=f"{guild.owner.name}", inline=False)
        em1.add_field(name="Server Besitzer ID", value=f"```{guild.owner.id}```", inline=False)
        em1.add_field(name="Server Mitglieder", value=f"{member_count}", inline=False)
        
        if guild.icon:
            em1.set_thumbnail(url=guild.icon.url)

        em1.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)

        file2 = discord.File("img/Imageline.png", filename="Imageline.png")
        em1.set_image(url="attachment://Imageline.png")

        try:
            await owner.send(embeds=[em0, em1], files=[file1, file2])
        
        except discord.Forbidden:
            print(f"Konnte keine DM an {owner} senden. DMs sind möglicherweise deaktiviert.")


    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        async with aiosqlite.connect("data/newguilds.db") as db:
            await db.execute('''
                UPDATE guilds SET guild_name = ?, guild_owner = ?, guild_owner_id = ?, guild_members = ? WHERE guild_id = ?
            ''', (after.name, after.owner.name, after.owner.id, sum(not member.bot for member in after.members), after.id))
            await db.commit()


def setup(bot: discord.Bot):
    bot.add_cog(JoinNewGuild(bot))