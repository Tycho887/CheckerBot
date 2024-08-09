from discord.ext import commands
import discord
from API_key.token import DISCORD_BOT_TOKEN
from lib import DatabaseManager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz


PUBLIC_KEY = "19a955916554f439298ec71eaf54f651e04b13bcdc48bff5514302f4bb71fc0a"

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

DB = DatabaseManager()

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

    if DB.add_user(user_id, user_name):
        await ctx.send(f"Opted in successfully!")
    else:
        await ctx.send(f"User already opted in!")

@bot.command()
async def optout(ctx):
    user_id = ctx.author.id

    if DB.remove_user(user_id):
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



def schedule_daily_message(hour, minute, timezone_str):
    print(f"Scheduling daily message at {hour}:{minute} in timezone {timezone_str}")
    timezone = pytz.timezone(timezone_str)
    scheduler.add_job(send_daily_message, CronTrigger(hour=hour, minute=minute, timezone=timezone))

# Schedule the message for 10 PM in a specific timezone, e.g., UTC
schedule_daily_message(13, 58, 'Europe/Oslo')


bot.run(DISCORD_BOT_TOKEN)
