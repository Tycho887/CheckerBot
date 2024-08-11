import discord
from discord.ext import commands
import logging
from lib.utility import schedule_daily_message, start_scheduler, get_bot_token, get_public_key
import lib.database as db
from lib.LLM import analyse_message_with_LLM

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load Discord bot credentials
DISCORD_BOT_TOKEN = get_bot_token()
DISCORD_PUBLIC_KEY = get_public_key()

# Initialize the bot
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    start_scheduler()
    logging.info(f'Logged in as {bot.user.name}')

# Global error handler
@bot.event
async def on_command_error(ctx, error):
    logging.error(f"An error occurred: {error}")
    await ctx.send("An error occurred while processing your request. Please try again.")

# Command Group: User-related commands
@bot.group()
async def user(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send('Invalid user command passed.')

@user.command(name="optin")
async def optin_user(ctx):
    user_id = ctx.author.id
    user_name = ctx.author.name
    logging.info(f"Opting in user {user_name} with ID {user_id}")

    if db.add_user(user_id, user_name):
        await ctx.send("Opted in successfully!")
    else:
        await ctx.send("User already opted in!")

@user.command(name="optout")
async def optout_user(ctx):
    user_id = ctx.author.id
    logging.info(f"Opting out user with ID {user_id}")

    if db.remove_user(user_id):
        await ctx.send("Opted out successfully!")
    else:
        await ctx.send("User not found!")

# Basic Command: Ping
@bot.command(name="ping")
async def ping_channel(ctx):
    await ctx.send('Pong!')

# Command: Analyze and store user response
@bot.command(name="mydaywas")
async def analyse_and_store_response(ctx, *args):
    message = " ".join(args)

    if len(message) < 50:
        await ctx.send(f"Please provide a longer message (at least 50 characters). You provided {len(message)} characters.")
        return

    await ctx.send("Thank you for sharing your feelings today!")
    analysis = analyse_message_with_LLM(message)
    db.add_data_to_records(ctx.author.id, analysis, message)
    logging.info(f"Stored analysis for user {ctx.author.name} with ID {ctx.author.id}")

# Command: Get user's data for the last 7 days and display it in a chart

@bot.command(name="myweek")




# Function: Send reminder to all users
async def send_reminder_to_all_users():
    users = db.get_users()
    for user in users:
        discord_user = await bot.fetch_user(user[0])
        if discord_user:
            try:
                await discord_user.send("Hello! How are you feeling today?")
                logging.info(f"Sent reminder to user with ID {user[0]}")
            except Exception as e:
                logging.error(f"Failed to send reminder to user {user[0]}: {e}")

# Schedule the daily reminder at a specific time (e.g., 8:18 PM UTC)
schedule_daily_message(20, 18, 'Europe/Oslo', send_reminder_to_all_users)



# Start the bot
bot.run(DISCORD_BOT_TOKEN)
