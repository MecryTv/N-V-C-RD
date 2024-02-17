import discord
import aiosqlite

from discord.ext import commands
from discord.commands import SlashCommandGroup
from utils.config import *
from datetime import datetime

class SetupServer(commands.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        async with aiosqlite.connect("data/server.db") as db:
            await db.execute("""
            CREATE TABLE IF NOT EXISTS server_settings (
                guild_id INTEGER PRIMARY KEY,
                join_and_leave_log_channel_id INTEGER,
                ticket_log_channel_id INTEGER,
                voice_log_channel_id INTEGER,
                member_log_channel_id INTEGER,
                mod_log_channel_id INTEGER,
                message_log_channel_id INTEGER,
                channel_log_channel_id INTEGER
            )""")
            await db.commit()

    setupgroup = SlashCommandGroup("setup")
    @setupgroup.command(description="Setup the Server")
    @commands.has_permissions(administrator=True)
    async def auditlogs(self, ctx):
        await ctx.defer()

        if commands.bot_has_permissions(administrator=True):
            async with aiosqlite.connect("data/server.db") as db:
                await db.execute("INSERT OR IGNORE INTO server_settings (guild_id) VALUES (?)", (ctx.guild.id,))
                await db.commit()
        
            em0 = discord.Embed(color=MainColor)
            file0 = discord.File("img/Auditlogs.png", filename="Auditlogs.png")
            em0.set_image(url="attachment://Auditlogs.png")

            em1 = discord.Embed(
                title="Server Setup Auditlogs",
                description="This is the setup for the server's audit logs",
                color=MainColor,
                timestamp=datetime.now(),
            )
            em1.add_field(name="Join and Leave Log", value="This will log all the members that join and leave the server", inline=False)
            em1.add_field(name="Ticket Log", value="This will log all the tickets that are created and closed", inline=False)
            em1.add_field(name="Voice Log", value="This will log all the voice channels that are joined and leaved", inline=False)
            em1.add_field(name="Member Log", value="This will log all the member Updates (Name, PFP, etc)", inline=False)
            em1.add_field(name="Mod Log", value="This will log all the moderation commands that are used", inline=False)
            em1.add_field(name="Message Log", value="This will log all the messages that are deleted and edited", inline=False)
            em1.add_field(name="Channel Log", value="This will log all the channels that are created and deleted", inline=False)
            file1 = discord.File("img/Imageline.png", filename="Imageline.png")
            em1.set_image(url="attachment://Imageline.png")
            em1.set_footer(text=self.bot.user.name, icon_url=self.bot.user.avatar.url)
            em1.set_thumbnail(url=self.bot.user.avatar.url)

            await ctx.respond(embeds=[em0, em1], files=[file0, file1], view=CreateDeleteEditSelectMenu(self.bot))


def setup(bot: discord.Bot):
    bot.add_cog(SetupServer(bot))


class CreateDeleteEditSelectMenu(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    options = [
        discord.SelectOption(
            label="Create",
            description="This will log all the messages that are created"
        ),
        discord.SelectOption(
            label="Delete",
            description="This will log all the messages that are deleted"
        ),
        discord.SelectOption(
            label="Edit",
            description="This will log all the messages that are edited"
        )
    ]

    @discord.ui.select(
        placeholder="Select the Log you want to setup",
        options=options,
        custom_id="create_delete_edit_select",
        max_values=1,
        min_values=1
    )

    async def callback(self, select, interaction):
            
            selected_option = select.values[0]
    
            if selected_option == "Create":
                await interaction.response.send_message(view=AuditlogsSelectMenu(self.bot))
    
            elif selected_option == "Delete":
                await interaction.response.send_message(view=DeleteSelectMenu())
    
            elif selected_option == "Edit":
                await interaction.response.send_message(view=EditSelectMenu())


class AuditlogsSelectMenu(discord.ui.View):
    def __init__(self, bot):
        super().__init__(timeout=None)
        self.bot = bot

    options = [
        discord.SelectOption(
            label="Join and Leave Log",
            description="This will log all the members that join and leave the server"
        ),
        discord.SelectOption(
            label="Ticket Log",
            description="This will log all the tickets that are created and closed"
        ),
        discord.SelectOption(
            label="Voice Log",
            description="This will log all the voice channels that are joined and leaved"
        ),
        discord.SelectOption(
            label="Member Log",
            description="This will log all the member Updates (Name, PFP, etc)"
        ),
        discord.SelectOption(
            label="Mod Log",
            description="This will log all the moderation commands that are used"
        ),
        discord.SelectOption(
            label="Message Log",
            description="This will log all the messages that are deleted and edited"
        ),
        discord.SelectOption(
            label="Channel Log",
            description="This will log all the channels that are created and deleted"
        )
    ]

    @discord.ui.select(
        placeholder="Select the Log you want to setup",
        options=options,
        custom_id="auditlogs_select",
        max_values=1,
        min_values=1
    )

    async def callback(self, select, interaction):
        
        selected_option = select.values[0]

        if selected_option == "Join and Leave Log":
            await interaction.response.send_message(view=JoinAndLeaveSelectMenu(), ephemeral=True)

        elif selected_option == "Ticket Log":
            await interaction.response.send_message(view=TicketSelectMenu(), ephemeral=True)

        elif selected_option == "Voice Log":
            await interaction.response.send_message(view=VoiceSelectMenu(), ephemeral=True)

        elif selected_option == "Member Log":
            await interaction.response.send_message(view=MemberSelectMenu(), ephemeral=True)

        elif selected_option == "Mod Log":
            await interaction.response.send_message(view=ModSelectMenu(), ephemeral=True)

        elif selected_option == "Message Log":
            await interaction.response.send_message(view=MessageSelectMenu(), ephemeral=True)

        elif selected_option == "Channel Log":
            await interaction.response.send_message(view=ChannelSelectMenu(), ephemeral=True)


async def get_join_and_leave_log_channel_id(self):
    async with aiosqlite.connect("data/server.db") as db:
        cursor = await db.execute("SELECT join_and_leave_log_channel_id FROM server_settings")
        result = await cursor.fetchone()
        return result[0] if result else None
    

async def get_ticket_log_channel_id(self):
    async with aiosqlite.connect("data/server.db") as db:
        cursor = await db.execute("SELECT ticket_log_channel_id FROM server_settings")
        result = await cursor.fetchone()
        return result[0] if result else None
    

async def get_voice_log_channel_id(self):
    async with aiosqlite.connect("data/server.db") as db:
        cursor = await db.execute("SELECT voice_log_channel_id FROM server_settings")
        result = await cursor.fetchone()
        return result[0] if result else None
    

async def get_member_log_channel_id(self):
    async with aiosqlite.connect("data/server.db") as db:
        cursor = await db.execute("SELECT member_log_channel_id FROM server_settings")
        result = await cursor.fetchone()
        return result[0] if result else None
    

async def get_mod_log_channel_id(self):
    async with aiosqlite.connect("data/server.db") as db:
        cursor = await db.execute("SELECT mod_log_channel_id FROM server_settings")
        result = await cursor.fetchone()
        return result[0] if result else None
    

async def get_message_log_channel_id(self):
    async with aiosqlite.connect("data/server.db") as db:
        cursor = await db.execute("SELECT message_log_channel_id FROM server_settings")
        result = await cursor.fetchone()
        return result[0] if result else None
    

async def get_channel_log_channel_id(self):
    async with aiosqlite.connect("data/server.db") as db:
        cursor = await db.execute("SELECT channel_log_channel_id FROM server_settings")
        result = await cursor.fetchone()
        return result[0] if result else None
    

class JoinAndLeaveSelectMenu(discord.ui.View):

    @discord.ui.channel_select(
        placeholder="Select a channel",
        custom_id="channel_select",
        min_values=1,
        max_values=1,
        channel_types=[discord.ChannelType.text]
    )
    async def callback(self, select, interaction):
        existing_channel_id = await self.get_join_and_leave_log_channel_id()

        if existing_channel_id:
            await interaction.response.send_message(f"Join and leave log channel already set: <#{existing_channel_id}>", ephemeral=True)
        else:
            async with aiosqlite.connect("data/server.db") as db:
                await db.execute("INSERT INTO server_settings (join_and_leave_log_channel_id) VALUES (?)", (select.values[0].id,))
                await db.commit()

            await interaction.response.send_message(f"Selected channel: {select.values[0].mention}", ephemeral=True)



class TicketSelectMenu(discord.ui.View):
    @discord.ui.channel_select(
        placeholder="Select a channel",
        custom_id="channel_select",
        min_values=1,
        max_values=1,
        channel_types=[discord.ChannelType.text]
    )
    async def callback(self, select, interaction):
        existing_channel_id = await self.get_ticket_log_channel_id()

        if existing_channel_id:
            await interaction.response.send_message(f"Join and leave log channel already set: <#{existing_channel_id}>", ephemeral=True)

        else:
            async with aiosqlite.connect("data/server.db") as db:
                await db.execute("INSERT INTO server_settings (ticket_log_channel_id) VALUES (?)", (select.values[0].id,))
                await db.commit()

            await interaction.response.send_message(f"Selected channel: {select.values[0].mention}", ephemeral=True)


class VoiceSelectMenu(discord.ui.View):
    @discord.ui.channel_select(
        placeholder="Select a channel",
        custom_id="channel_select",
        min_values=1,
        max_values=1,
        channel_types=[discord.ChannelType.text]
    )
    async def callback(self, select, interaction):
        existing_channel_id = await self.get_voice_log_channel_id()

        if existing_channel_id:
            await interaction.response.send_message(f"Join and leave log channel already set: <#{existing_channel_id}>", ephemeral=True)

        else:
            async with aiosqlite.connect("data/server.db") as db:
                await db.execute("INSERT INTO server_settings (voice_log_channel_id) VALUES (?)", (select.values[0].id,))
                await db.commit()

            await interaction.response.send_message(f"Selected channel: {select.values[0].mention}", ephemeral=True)


class MemberSelectMenu(discord.ui.View):
    @discord.ui.channel_select(
        placeholder="Select a channel",
        custom_id="channel_select",
        min_values=1,
        max_values=1,
        channel_types=[discord.ChannelType.text]
    )
    async def callback(self, select, interaction):
        existing_channel_id = await self.get_member_log_channel_id()

        if existing_channel_id:
            await interaction.response.send_message(f"Join and leave log channel already set: <#{existing_channel_id}>", ephemeral=True)

        else:
            async with aiosqlite.connect("data/server.db") as db:
                await db.execute("INSERT INTO server_settings (member_log_channel_id) VALUES (?)", (select.values[0].id,))
                await db.commit()

            await interaction.response.send_message(f"Selected channel: {select.values[0].mention}", ephemeral=True)


class ModSelectMenu(discord.ui.View):
    @discord.ui.channel_select(
        placeholder="Select a channel",
        custom_id="channel_select",
        min_values=1,
        max_values=1,
        channel_types=[discord.ChannelType.text]
    )
    async def callback(self, select, interaction):
        existing_channel_id = await self.get_mod_log_channel_id()

        if existing_channel_id:
            await interaction.response.send_message(f"Join and leave log channel already set: <#{existing_channel_id}>", ephemeral=True)

        else:
            async with aiosqlite.connect("data/server.db") as db:
                await db.execute("INSERT INTO server_settings (mod_log_channel_id) VALUES (?)", (select.values[0].id,))
                await db.commit()

            await interaction.response.send_message(f"Selected channel: {select.values[0].mention}", ephemeral=True)


class MessageSelectMenu(discord.ui.View):
    @discord.ui.channel_select(
        placeholder="Select a channel",
        custom_id="channel_select",
        min_values=1,
        max_values=1,
        channel_types=[discord.ChannelType.text]
    )
    async def callback(self, select, interaction):
        existing_channel_id = await self.get_message_log_channel_id()

        if existing_channel_id:
            await interaction.response.send_message(f"Join and leave log channel already set: <#{existing_channel_id}>", ephemeral=True)

        else:
            async with aiosqlite.connect("data/server.db") as db:
                await db.execute("INSERT INTO server_settings (message_log_channel_id) VALUES (?)", (select.values[0].id,))
                await db.commit()

            await interaction.response.send_message(f"Selected channel: {select.values[0].mention}", ephemeral=True)


class ChannelSelectMenu(discord.ui.View):
    @discord.ui.channel_select(
        placeholder="Select a channel",
        custom_id="channel_select",
        min_values=1,
        max_values=1,
        channel_types=[discord.ChannelType.text]
    )
    async def callback(self, select, interaction):
        existing_channel_id = await self.get_channel_log_channel_id()

        if existing_channel_id:
            await interaction.response.send_message(f"Join and leave log channel already set: <#{existing_channel_id}>", ephemeral=True)

        else:
            async with aiosqlite.connect("data/server.db") as db:
                await db.execute("INSERT INTO server_settings (channel_log_channel_id) VALUES (?)", (select.values[0].id,))
                await db.commit()

            await interaction.response.send_message(f"Selected channel: {select.values[0].mention}", ephemeral=True)