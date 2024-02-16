import discord
import ezcord
import os

from dotenv import load_dotenv


class Bot(ezcord.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(intents=intents, language="de")

        self.load_cogs("cogs", subdirectories=True)

    def run(self):
        load_dotenv()
        super().run(os.getenv("TOKEN"))
