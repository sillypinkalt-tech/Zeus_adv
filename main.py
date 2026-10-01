```python
import os
import json
import discord
from discord import app_commands
import asyncio
import datetime

intents = discord.Intents.default()
intents.message_content = True

def load_config():
    try:
        with open('config.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def load_keys():
    try:
        with open('keys.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"keys": []}

def save_keys(keys):
    with open('keys.json', 'w') as f:
        json.dump(keys, f, indent=2)

def add_key_to_db(key):
    try:
        keys = load_keys()
        keys['keys'].append(key)
        save_keys(keys)
        return True
    except Exception as e:
        print(f"❌ Error adding key: {str(e)}")
        return False

client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@tree.command(name="generatekeyv1", description="Generate V1 key (1 user, 4 channels, 30 days)")
async def generatekeyv1(interaction):
    try:
        key = f"KEY_{datetime.datetime.now().timestamp()}"
        if add_key_to_db(key):
            await interaction.response.send_message(f"✅ Generated V1 key: {key}")
        else:
            await interaction.response.send_message("❌ Failed to generate key")
    except Exception as e:
        await interaction.response.send_message(f"❌ Error: {str(e)}")

@tree.command(name="generatekeyv2", description="Generate V2 key (2 users, 8 channels, 30 days)")
async def generatekeyv2(interaction):
    try:
        key = f"KEY_{datetime.datetime.now().timestamp()}"
        if add_key_to_db(key):
            await interaction.response.send_message(f"✅ Generated V2 key: {key}")
        else:
            await interaction.response.send_message("❌ Failed to generate key")
    except Exception as e:
        await interaction.response.send_message(f"❌ Error: {str(e)}")

@tree.command(name="generatekeyv3", description="Generate V3 key (5 users, 25 channels, 30 days)")
async def generatekeyv3(interaction):
    try:
        key = f"KEY_{datetime.datetime.now().timestamp()}"
        if add_key_to_db(key):
            await interaction.response.send_message(f"✅ Generated V3 key: {key}")
        else:
            await interaction.response.send_message("❌ Failed to generate key")
    except Exception as e:
        await interaction.response.send_message(f"❌ Error: {str(e)}")

async def main():
    if not os.getenv("BOT_TOKEN"):
        print("❌ Error: BOT_TOKEN environment variable is missing")
        return

    try:
        client.loop.create_task(tree.sync())
        await client.start(os.getenv("BOT_TOKEN"))
    except Exception as e:
        print(f"❌ Failed to start bot: {str(e)}")

if __name__ == "__main__":
    asyncio.run(main())
```
