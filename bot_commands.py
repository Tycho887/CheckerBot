from lib.LLM import analyse_message_with_LLM
import lib.database as db

async def ping_channel(ctx):
    await ctx.send('Pong!')

async def optin_user(ctx):
    user_id = ctx.author.id
    user_name = ctx.author.name
    print(user_id, user_name)
    if db.add_user(user_id, user_name):
        await ctx.send(f"Opted in successfully!")
    else:
        await ctx.send(f"User already opted in!")

async def optout_user(ctx):
    user_id = ctx.author.id
    if db.remove_user(user_id):
        await ctx.send(f"Opted out successfully!")
    else:
        await ctx.send(f"User not found!")

async def analyse_and_store_response(ctx, *args):

    message = " ".join(args)

    if len(message) < 50:
        await ctx.send(f"Could you please provide a longer message? I need at least 50 characters to analyse your message, and you only provided {len(message)} characters.")
        return
    else:
        await ctx.send("Thank you for sharing your feelings today!")

        analysis = analyse_message_with_LLM(message)

        db.add_data_to_records(ctx.author.id, analysis, message)

async def send_reminder_to_all_users(bot):
    users = db.get_users()
    for user in users:
        # if the user_id does not correspond to a valid user, we want to skip this iteration
        if not bot.get_user(user[0]):
            continue

        user = await bot.fetch_user(user[0])
        await user.send(f"Hello! How are you feeling today?")

