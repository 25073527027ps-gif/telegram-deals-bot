import os
import time
from telegram import Bot

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)

print("Bot is running successfully...")

while True:
    time.sleep(10)
