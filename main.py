from discord.ext import commands
import discord
from lib.utility import schedule_daily_message, start_scheduler  # Import functions from the scheduler module
from lib.database import add_user, remove_user, get_users, get_all_records, add_data_to_records, get_records_for_user
from lib.utility import get_bot_token, get_public_key
import bot_commands as bc

# import api key from .env file

DISCORD_BOT_TOKEN = get_bot_token()
DISCORD_PUBLIC_KEY = get_public_key()

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all())

# we want to create a try-except decorator

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    start_scheduler(bot)

@bot.command()
async def ping(ctx):
    try:
        bc.ping(ctx)
    except Exception as e:
        print(f"An error occured when pinging: {e}")

@bot.command()
async def optin(ctx):
    try:
        bc.optin(ctx)
    except Exception as e:
        print(f"An error occured when opting in user: {e}")

@bot.command()
async def optin(ctx):
    try:
        bc.optout(ctx)
    except Exception as e:
        print(f"An error occured when opting out user: {e}")


# Schedule the message for 10 PM in a specific timezone, e.g., UTC
schedule_daily_message(17, 30, 'Europe/Oslo', remind_users)

bot.run(DISCORD_BOT_TOKEN)
