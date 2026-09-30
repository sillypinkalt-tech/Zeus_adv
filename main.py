import os
import json
import discord
from discord import app_commands
import asyncio
import datetime

# Initialize Discord client
intents = discord.Intents.default()
intents.message_content = True  # Required for reading messages

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# Load configuration
def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Load keys
def load_keys():
    try:
        with open('keys.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"keys": []}

# Save keys
def save_keys(keys):
    with open('keys.json', 'w') as f:
        json.dump(keys, f, indent=2)

# Validate key
def validate_key(key):
    keys = load_keys()
    for k in keys['keys']:
        if k['key'] == key:
            return k
    return None

# Get plan details
def get_plan_details(plan):
    config = load_config()
    return config.get('plans', {}).get(plan, {})

# Main bot logic
async def main():
    # Load configuration
    config = load_config()
    keys = load_keys()
    
    # Check for missing bot token
    if not os.getenv("BOT_TOKEN"):
        print("❌ Error: BOT_TOKEN environment variable is missing")
        return
    
    # Initialize Discord client
    try:
        client.loop.create_task(tree.sync())  # Sync commands
        await client.start(os.getenv("BOT_TOKEN"))
    except Exception as e:
        print(f"❌ Failed to start bot: {str(e)}")
        return

# Run the bot
if __name__ == "__main__":
    asyncio.run(main())
