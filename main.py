from discord.ext import commands
import discord
from lib.utility import schedule_daily_message, start_scheduler  # Import functions from the scheduler module
from lib.database import add_user, remove_user, get_users, get_all_records, add_data_to_records, get_records_for_user
from lib.utility import get_bot_token, get_public_key

# import api key from .env file

DISCORD_BOT_TOKEN = get_bot_token()
DISCORD_PUBLIC_KEY = get_public_key()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    start_scheduler()
    print(f"Bot is ready, logged in as {bot.user}") 

@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

@bot.command()
async def optin(ctx):
    user_id = ctx.author.id
    user_name = ctx.author.name
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

@bot.command()
async def daily(ctx, message):
    # This is the command that the user uses to answer the daily message
    user_id = ctx.author.id

# async def send_daily_message(ctx,user_id):
#     try:
#         user = await bot.fetch_user(user_id)
#         if user:
#             await user.send(f"Hello! How are you feeling today?")
#     except Exception as e:
#         print(f"Failed to send message to user {user_id}")
#         return False

async def remind_users():
    users = get_users()
    print(users)
    for user_id, user_name in users:
        try:
            user = await bot.fetch_user(user_id)
            if user:
                await user.send(f"Hello! How are you feeling today?")
        except Exception as e:
            print(f"Failed to send message to user {user_id}")
            continue

# Schedule the message for 10 PM in a specific timezone, e.g., UTC
schedule_daily_message(17, 30, 'Europe/Oslo', remind_users)

bot.run(DISCORD_BOT_TOKEN)
