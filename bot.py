import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_ID = "@dealsoffreedom"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🔥 Send Amazon Affiliate Link"
    )

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    link = update.message.text.strip()

    if "amazon" in link or "amzn.to" in link:

        message = f"""
🔥 HOT AMAZON DEAL 🔥

💥 Limited Time Offer
⚡ Best Price Online

👉 Buy Now:
{link}

📢 Join:
https://t.me/dealsoffreedom
"""

        # SEND TO CHANNEL
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=message,
            disable_web_page_preview=False
        )

        await update.message.reply_text(
            "✅ Deal Sent To Channel"
        )

    else:

        await update.message.reply_text(
            "❌ Send Valid Amazon Link"
        )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link)
)

print("🚀 Bot Running...")

app.run_polling()
