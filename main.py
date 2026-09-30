import discord
from discord import app_commands
import json
import datetime
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

config = json.load(open('config.json'))
keys_db = json.load(open('keys.json'))

def validate_key(key):
    for k in keys_db['keys']:
        if k['key'] == key:
            return k
    return None

def get_plan_details(plan):
    return config['plans'].get(plan)

def add_key_to_db(key):
    keys_db['keys'].append(key)
    with open('keys.json', 'w') as f:
        json.dump(keys_db, f)

async def send_ad_message(channel_id, message, interval):
    while True:
        try:
            channel = await client.fetch_channel(channel_id)
            await channel.send(message)
            await asyncio.sleep(interval)
        except Exception as e:
            print(f"Error sending message: {e}")
            break

@tree.command(name="generatekeyv1", description="Generate V1 key (1 user, 4 channels, 1 month)")
async def generate_key_v1(interaction):
    key = {
        "key": f"V1-{os.urandom(16).hex()}-{os.urandom(16).hex()}",
        "plan": "V1",
        "users": 1,
        "channels": 4,
        "expires": (datetime.datetime.now() + datetime.timedelta(days=30)).strftime("%Y-%m-%d"),
        "user_tokens": [],
        "ad_channels": []
    }
    add_key_to_db(key)
    await interaction.response.send_message(f"Generated V1 key: `{key['key']}`")

@tree.command(name="panel", description="Access your advertising panel")
async def panel(interaction):
    await interaction.response.send_message("Welcome to your advertising panel! Use /addkey to activate your subscription.")

@tree.command(name="addkey", description="Add your subscription key")
async def add_key(interaction, key: str):
    key_data = validate_key(key)
    if not key_data:
        await interaction.response.send_message("Invalid key! Please check the key and try again.")
        return
    
    plan = key_data['plan']
    plan_details = get_plan_details(plan)
    
    if not plan_details:
        await interaction.response.send_message("Invalid key plan! Please contact support.")
        return
    
    await interaction.response.send_message(f"Key validated! You have access to {plan_details['users']} users and {plan_details['channels']} channels.")
    
    # Here you would add logic to let the user configure their advertising settings

# Run the bot
client.run(config['bot_token'])
