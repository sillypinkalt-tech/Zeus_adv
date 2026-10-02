import os
import sqlite3
from datetime import datetime, timedelta

import discord
from discord.ext import commands

from keys import generate_key

TOKEN = os.getenv("BOT_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)


def get_db():
    return sqlite3.connect("zeus_adv.db")


def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS subscriptions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        plan_type TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS keys (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        key TEXT NOT NULL UNIQUE,
        user_id TEXT NULL,
        plan_type TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP NULL
    )""")

    cur.execute("""CREATE TABLE IF NOT EXISTS campaigns (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id TEXT NOT NULL,
        name TEXT NOT NULL,
        sending_account TEXT NOT NULL,
        channels TEXT NOT NULL,
        message TEXT NOT NULL,
        interval INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'stopped'
    )""")

    conn.commit()
    conn.close()


def parse_datetime(value):
    if isinstance(value, datetime):
        return value
    if not value:
        return None
    try:
        return datetime.fromisoformat(str(value))
    except ValueError:
        return None


def get_active_subscription(user_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, user_id, plan_type, created_at, expires_at "
        "FROM subscriptions WHERE user_id = ? ORDER BY id DESC LIMIT 1",
        (str(user_id),),
    )
    row = cur.fetchone()
    conn.close()
    if not row:
        return None
    expires_at = parse_datetime(row[4])
    if expires_at and expires_at <= datetime.now():
        return None
    return row


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} (ID: {bot.user.id})")
    print("Bot is ready!")


@bot.command(name="panel")
async def panel(ctx):
    subscription = get_active_subscription(ctx.author.id)
    embed = discord.Embed(title="Panel", color=0x00FF00)
    embed.add_field(name="Subscription", value="View your plan", inline=False)
    embed.add_field(name="Sending Accounts", value="Manage sending accounts", inline=False)
    embed.add_field(name="Channels", value="Manage channels", inline=False)
    embed.add_field(name="Campaigns", value="Manage campaigns", inline=False)
    embed.add_field(name="Redeem Key", value="Use your subscription key", inline=False)

    if subscription:
        expires_at = parse_datetime(subscription[4])
        days = max(0, (expires_at - datetime.now()).days) if expires_at else 0
        embed.add_field(
            name="Current Plan",
            value=f"{subscription[2]} — {days} days remaining",
            inline=False,
        )
    else:
        embed.add_field(name="Current Plan", value="No active subscription", inline=False)

    await ctx.send(embed=embed)


@bot.command(name="redeem")
async def redeem(ctx, key: str):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, key, user_id, plan_type FROM keys WHERE key = ?",
        (key,),
    )
    key_data = cur.fetchone()

    if not key_data:
        conn.close()
        await ctx.send("Invalid key.")
        return

    if key_data[2] is not None:
        conn.close()
        await ctx.send("Key already used.")
        return

    now = datetime.now()
    expires = now + timedelta(days=30)
    user_id = str(ctx.author.id)

    cur.execute(
        "UPDATE keys SET user_id = ?, expires_at = ? WHERE id = ?",
        (user_id, expires.isoformat(), key_data[0]),
    )
    cur.execute(
        "INSERT INTO subscriptions (user_id, plan_type, created_at, expires_at) "
        "VALUES (?, ?, ?, ?)",
        (user_id, key_data[3], now.isoformat(), expires.isoformat()),
    )
    conn.commit()
    conn.close()
    await ctx.send("Subscription activated for 30 days.")


@bot.command(name="generatekeyv1")
async def generate_key_v1(ctx):
    key = generate_key("v1")
    await ctx.send(f"Generated key: {key}")


@bot.command(name="generatekeyv2")
async def generate_key_v2(ctx):
    key = generate_key("v2")
    await ctx.send(f"Generated key: {key}")


@bot.command(name="generatekeyv3")
async def generate_key_v3(ctx):
    key = generate_key("v3")
    await ctx.send(f"Generated key: {key}")


if __name__ == "__main__":
    init_db()
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN environment variable is not set.")
    bot.run(TOKEN)
