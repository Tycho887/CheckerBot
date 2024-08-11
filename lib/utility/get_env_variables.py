import os
from dotenv import load_dotenv

load_dotenv()

def get_public_key():
    return os.getenv("DISCORD_PUBLIC_KEY")

def get_bot_token():
    return os.getenv("DISCORD_BOT_TOKEN")

def get_open_ai_key():
    return os.getenv("OPEN_AI_API_KEY")