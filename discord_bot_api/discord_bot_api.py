import os

import discord
from dotenv import load_dotenv
from flask import Flask, request, jsonify
import threading

# Discord bot setup
intents = discord.Intents.default()
client = discord.Client(intents=intents)
load_dotenv()
TOKEN = os.getenv("DISCORD_BOT_TOKEN")

# Flask setup
app = Flask(__name__)


@app.route('/', methods=['POST'])
def send_message():
    data = request.get_json()
    if 'message' not in data:
        return jsonify({'error': 'Message is required'}), 400
    message = data['message']

    async def send_to_discord():
        for guild in client.guilds:
            for channel in guild.text_channels:
                try:
                    await channel.send(message)
                except discord.Forbidden:
                    print(f"Cannot send message to {channel.name} in {guild.name} (no permissions).")
                except discord.HTTPException as e:
                    print(f"Failed to send message to {channel.name} in {guild.name}: {e}")

    client.loop.create_task(send_to_discord())
    return jsonify({'status': 'Message sent to Discord'})


# Run Flask in a separate thread
def run_flask():
    app.run(host='127.0.0.1', port=5000)


flask_thread = threading.Thread(target=run_flask)
flask_thread.start()


# Run Discord bot
@client.event
async def on_ready():
    print(f'Bot connected as {client.user}')


client.run(TOKEN)