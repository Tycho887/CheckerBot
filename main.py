from discord.ext import commands
import discord
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from lib import analyse_message_with_LLM, get_bot_token, get_public_key, add_data_to_records, add_user, remove_user
import pytz

# import api key from .env file

DISCORD_BOT_TOKEN = get_bot_token()
DISCORD_PUBLIC_KEY = get_public_key()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())


scheduler = AsyncIOScheduler()

@bot.event
async def on_ready():
    scheduler.start()
    print(f"Bot is ready, logged in as {bot.user}") 

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def optin(ctx):
    user_id = ctx.author.id

    user_name = ctx.author.name[:-4]

    print(user_id, user_name)

    if add_user(user_id, user_name):
        await ctx.send(f"Opted in successfully!")
    else:
        await ctx.send(f"User already opted in!")

@bot.command()
async def optout(ctx):
    user_id = ctx.author.id

    if remove_user(user_id):
        await ctx.send(f"Opted out successfully!")
    else:
        await ctx.send(f"User not found!")

async def send_daily_message():

    users = DB.get_users()

    print(users)

    for user_id, user_name in users:
        user = await bot.fetch_user(user_id)
        if user:
            await user.send(f"Hello {user_name}! How are you feeling today?")

# We want to detect messages sent in DMs

@bot.command()
async def daily(ctx, message):
    # This is the command that the user uses to answer the daily message

    user_id = ctx.author.id

def schedule_daily_message(hour, minute, timezone_str):
    print(f"Scheduling daily message at {hour}:{minute} in timezone {timezone_str}")
    timezone = pytz.timezone(timezone_str)
    scheduler.add_job(send_daily_message, CronTrigger(hour=hour, minute=minute, timezone=timezone))

# Schedule the message for 10 PM in a specific timezone, e.g., UTC
schedule_daily_message(22, 0, 'Europe/Oslo')


bot.run(DISCORD_BOT_TOKEN)
