from lib.utility import schedule_daily_message, start_scheduler  # Import functions from the scheduler module
from lib.LLM import LLM
import lib.database as db
from discord.ext import commands
import discord
from lib.utility import get_bot_token, get_public_key

async def ping(ctx):
    await ctx.send('Pong!')

async def optin(ctx):
    user_id = ctx.author.id
    user_name = ctx.author.name
    print(user_id, user_name)
    if db.add_user(user_id, user_name):
        await ctx.send(f"Opted in successfully!")
    else:
        await ctx.send(f"User already opted in!")

async def optout(ctx):
    user_id = ctx.author.id
    if db.remove_user(user_id):
        await ctx.send(f"Opted out successfully!")
    else:
        await ctx.send(f"User not found!")

async def daily(ctx, message):
    if len(message) < 50:
        await ctx.send("Could you please provide a longer message?")
        return
    else:
        ctx.send("Thank you for sharing your feelings today!")

        analysis = LLM.analyse_message_with_LLM(message)

        db.add_data_to_records(ctx.author.id, analysis, message)

async def loop_through_users(bot):
    users = db.get_users()
    for user in users:
        # if the user_id does not correspond to a valid user, we want to skip this iteration
        if not bot.get_user(user[0]):
            continue

        user = await bot.fetch_user(user[0])
        await user.send(f"Hello! How are you feeling today?")

