# This example requires the 'message_content' intent.
import os

import discord
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
def send_flip(text: str) -> None:
    for guild in client.guilds:
        for channel in guild.text_channels:
            try:
                channel.send(text)
            except discord.Forbidden:
                print(f"Cannot send message to {channel.name} in {guild.name} (no permissions).")
            except discord.HTTPException as e:
                print(f"Failed to send message to {channel.name} in {guild.name}: {e}")

client.run(os.getenv("DISCORD_BOT_TOKEN"))
