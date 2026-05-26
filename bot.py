import os
from telegram import Bot

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)

print("Bot is running successfully...")
