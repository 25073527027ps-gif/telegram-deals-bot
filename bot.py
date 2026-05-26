import os
import time
from telegram import Bot

TOKEN = os.getenv("8601951285:AAE09-x_4Peuh3WSJN68U21iGFKsCuVnLLE")

bot = Bot(token=TOKEN)

print("Bot is running successfully...")

while True:
    time.sleep(10)
