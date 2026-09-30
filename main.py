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

def add_key
