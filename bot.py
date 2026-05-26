import os
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# ====================================
# SETTINGS
# ====================================

TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_ID = "@dealsoffreedom"

# ====================================
# START
# ====================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 Send Amazon Affiliate Link 🔥"
    )

# ====================================
# HANDLE LINKS
# ====================================

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    link = update.message.text.strip()

    # AMAZON LINK CHECK
    if "amazon" in link or "amzn.to" in link:

        # BUTTON
        buttons = [
            [
                InlineKeyboardButton(
                    "🛒 Buy Now",
                    url=link
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(buttons)

        # CLEAN MESSAGE
        message = """
🔥 HOT AMAZON DEAL 🔥

💥 Limited Time Offer
⚡ Best Price Online

👇 Buy From Button Below
"""

        # SEND TO CHANNEL
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=message,
            reply_markup=reply_markup,
            disable_web_page_preview=False
        )

        # SEND LINK FOR REAL PRODUCT PREVIEW
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=link,
            disable_web_page_preview=False
        )

        await update.message.reply_text(
            "✅ Deal Posted Successfully 🚀"
        )

    else:

        await update.message.reply_text(
            "❌ Send Valid Amazon Link"
        )

# ====================================
# MAIN
# ====================================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link)
)

print("🚀 Amazon Deals Bot Running...")

app.run_polling()
