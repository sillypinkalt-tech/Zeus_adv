import os
import discord
from discord.ext import commands
import sqlite3
import asyncio
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)
from discord.ui import View, Button
from discord import Embed

@bot.command(name='panel')
async def panel(ctx):
    embed = Embed(title='Panel', color=0x00ff00)
    embed.add_field(name='Subscription', value='Click to view your plan', inline=False)
    embed.add_field(name='Sending Accounts', value='Coming soon', inline=False)
    embed.add_field(name='Channels', value='Coming soon', inline=False)
    embed.add_field(name='Campaigns', value='Coming soon', inline=False)
    embed.add_field(name='Redeem Key', value='Enter a key to activate your subscription', inline=False)
    view = View()
    subscription_btn = Button(label='Subscription', style=ButtonStyle.green)
    subscription_btn.callback = lambda i: get_subscription(i, ctx)
    view.add_item(subscription_btn)
    await ctx.send(embed=embed, view=view)

async def get_subscription(interaction, ctx):
    user_id = str(interaction.user.id)
    conn = sqlite3.connect('zeus_adv.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM subscriptions WHERE user_id = ?', (user_id,))
    subscription = cur.fetchone()
    cur.close()
    conn.close()
    
    if subscription:
        plan_type = subscription[2]
        activation_date = subscription[3]
        expiration_date = subscription[4]
        days_remaining = (expiration_date - datetime.now()).days
        embed = Embed(title='Subscription', color=0x00ff00)
        embed.add_field(name='Plan', value=plan_type, inline=False)
        embed.add_field(name='Activation Date', value=activation_date.strftime('%Y-%m-%d'), inline=False)
        embed.add_field(name='Expiration Date', value=expiration_date.strftime('%Y-%m-%d'), inline=False)
        embed.add_field(name='Days Remaining', value=str(days_remaining), inline=False)
        await interaction.response.edit_message(embed=embed)
    else:
        await interaction.response.edit_message(content='No active subscription.')
from discord import Embed, Button, View
from discord.ui import Modal, InputText, button

@bot.command(name='panel')
async def panel(ctx):
    embed = Embed(title='Panel', color=0x00ff00)
    embed.add_field(name='Subscription', value='Click to view your plan', inline=False)
    embed.add_field(name='Sending Accounts', value='Coming soon', inline=False)
    embed.add_field(name='Channels', value='Coming soon', inline=False)
    embed.add_field(name='Campaigns', value='Coming soon', inline=False)
    embed.add_field(name='Redeem Key', value='Enter a key to activate your subscription', inline=False)
    await ctx.send(embed=embed)

@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return
    if msg.content == '/panel':
        await panel(msg)
        return
    if msg.channel.category_id == 123456789012345678:
        if msg.author == bot.user:
            return
        if msg.content.startswith('/panel'):
            await panel(msg)
            return
@bot.command(name='panel')
async def panel(ctx):
    await ctx.send('Please provide your key:')
    msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    key = msg.content.strip()
    
    conn = sqlite3.connect('zeus_adv.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM keys WHERE key = ?', (key,))
    key_data = cur.fetchone()
    cur.close()
    conn.close()
    
    if not key_data:
        await ctx.send('Invalid key.')
        return
    
    if key_data[3] is not None:
        await ctx.send('Key already used.')
        return
    
    plan_type = key_data[2]
    user_id = str(ctx.author.id)
    
    conn = sqlite3.connect('zeus_adv.db')
    cur = conn.cursor()
    cur.execute('UPDATE keys SET user_id = ?, expires_at = ? WHERE key = ?', (user_id, datetime.now() + timedelta(days=30), key))
    cur.execute('INSERT INTO subscriptions (user_id, plan_type, expires_at) VALUES (?, ?, ?)', (user_id, plan_type, datetime.now() + timedelta(days=30)))
    conn.commit()
    cur.close()
    conn.close()
    
    await ctx.send('Subscription activated.')
@bot.command(name='panel')
async def panel(ctx):
    await ctx.send('Please provide your key:')
    msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author and m.channel == ctx.channel)
    key = msg.content.strip()
    
    conn = sqlite3.connect('zeus_adv.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM keys WHERE key = ?', (key,))
    key_data = cur.fetchone()
    cur.close()
    conn.close()
    
    if not key_data:
        await ctx.send('Invalid key.')
        return
    
    if key_data[3] is not None:
        await ctx.send('Key already used.')
        return
    
    plan_type = key_data[2]
    user_id = str(ctx.author.id)
    
    conn = sqlite3.connect('zeus_adv.db')
    cur = conn.cursor()
    cur.execute('UPDATE keys SET user_id = ?, expires_at = ? WHERE key = ?', (user_id, datetime.now() + timedelta(days=30), key))
    cur.execute('INSERT INTO subscriptions (user_id, plan_type, expires_at) VALUES (?, ?, ?)', (user_id, plan_type, datetime.now() + timedelta(days=30)))
    conn.commit()
    cur.close()
    conn.close()
    
    await ctx.send('Subscription activated.')

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('Bot is ready!')

@bot.command(name='generatekeyv1')
async def generate_key_v1(ctx):
    from keys import generate_key
    key = generate_key('v1')
    await ctx.send(f'Generated key: {key}')

@bot.command(name='generatekeyv2')
async def generate_key_v2(ctx):
    from keys import generate_key
    key = generate_key('v2')
    await ctx.send(f'Generated key: {key}')

@bot.command(name='generatekeyv3')
async def generate_key_v3(ctx):
    from keys import generate_key
    key = generate_key('v3')
    await ctx.send(f'Generated key: {key}')

@bot.command(name='panel')
async def panel(ctx):
    await ctx.send('Panel commands coming soon!')
import os
import discord
from discord.ext import commands
import sqlite3
import random
import string
import asyncio
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Initialize database
conn = sqlite3.connect('zeus_adv.db')
cur = conn.cursor()

cur.execute(''
    CREATE TABLE IF NOT EXISTS subscriptions ("
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        plan_type TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP
    )
'')

cur.execute(''
    CREATE TABLE IF NOT EXISTS keys ("
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT NOT NULL UNIQUE,
        user_id TEXT NULL,
        plan_type TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP NULL
    )
'')

cur.execute(''
    CREATE TABLE IF NOT EXISTS campaigns ("
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        name TEXT NOT NULL,
        sending_account TEXT NOT NULL,
        channels TEXT NOT NULL,
        message TEXT NOT NULL,
        interval INT NOT NULL,
        status TEXT NOT NULL DEFAULT 'stopped'
    )
'')

conn.commit()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('Bot is ready!')

@bot.command(name='generatekeyv1')
async def generate_key_v1(ctx):
    key = generate_key('v1')
    await ctx.send(f'Generated key: {key}')

@bot.command(name='generatekeyv2')
async def generate_key_v2(ctx):
    key = generate_key('v2')
    await ctx.send(f'Generated key: {key}')

@bot.command(name='generatekeyv3')
async def generate_key_v3(ctx):
    key = generate_key('v3')
    await ctx.send(f'Generated key: {key}')

@bot.command(name='panel')
async def panel(ctx):
    await ctx.send('Panel commands coming soon!')

def generate_key(plan_type):
    conn = sqlite3.connect('zeus_adv.db')
    cur = conn.cursor()
    
    while True:
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        cur.execute('SELECT * FROM keys WHERE key = ?', (key,))
        if not cur.fetchone():
            # Store as pending with no expiration
            cur.execute(''
                INSERT INTO keys (key, plan_type)
                VALUES (?, ?)
            '', (key, plan_type))
            conn.commit()
            cur.close()
            conn.close()
            return key
        cur.close()
        conn.close()
import os
import discord
from discord.ext import commands
import sqlite3
import random
import string
import asyncio
from datetime import datetime, timedelta

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='/', intents=intents)

# Initialize database
conn = sqlite3.connect('zeus_adv.db')
cur = conn.cursor()

cur.execute(''
    CREATE TABLE IF NOT EXISTS subscriptions ("
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        plan_type TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP
    )
'')

cur.execute(''
    CREATE TABLE IF NOT EXISTS keys ("
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT NOT NULL UNIQUE,
        user_id TEXT NOT NULL,
        plan_type TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP
    )
'')

cur.execute(''
    CREATE TABLE IF NOT EXISTS campaigns ("
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        name TEXT NOT NULL,
        sending_account TEXT NOT NULL,
        channels TEXT NOT NULL,
        message TEXT NOT NULL,
        interval INT NOT NULL,
        status TEXT NOT NULL DEFAULT 'stopped'
    )
'')

conn.commit()

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('Bot is ready!')

@bot.command(name='generatekeyv1')
async def generate_key_v1(ctx):
    key = generate_key('v1')
    await ctx.send(f'Generated key: {key}')

@bot.command(name='generatekeyv2')
async def generate_key_v2(ctx):
    key = generate_key('v2')
    await ctx.send(f'Generated key: {key}')

@bot.command(name='generatekeyv3')
async def generate_key_v3(ctx):
    key = generate_key('v3')
    await ctx.send(f'Generated key: {key}')

@bot.command(name='panel')
async def panel(ctx):
    await ctx.send('Panel commands coming soon!')

def generate_key(plan_type):
    while True:
        key = ''.join(random.choices(string.ascii_letters + string.digits, k=20))
        cur.execute('SELECT * FROM keys WHERE key = ?', (key,))
        if not cur.fetchone():
            now = datetime.now()
            expires = now + timedelta(days=30)
            cur.execute(''
                INSERT INTO keys (key, user_id, plan_type, expires_at)
                VALUES (?, ?, ?, ?)
            '', (key, str(ctx.author.id), plan_type, expires))
            conn.commit()
            return key

bot.run(os.getenv('BOT_TOKEN'))
