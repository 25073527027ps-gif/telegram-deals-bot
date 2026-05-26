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

TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_ID = "@dealsoffreedom"

# ==========================================
# START COMMAND
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 Send Any Shopping Product Link 🔥"
    )

# ==========================================
# HANDLE LINKS
# ==========================================

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    link = update.message.text.strip()

    # ACCEPT ALL SHOPPING LINKS
    if (
        "amazon" in link
        or "amzn.to" in link
        or "flipkart" in link
        or "myntra" in link
        or "ajio" in link
        or "meesho" in link
    ):

        # BUTTONS
        keyboard = [
            [
                InlineKeyboardButton(
                    "🛒 Buy Now",
                    url=link
                )
            ],
            [
                InlineKeyboardButton(
                    "📢 Join Channel",
                    url="https://t.me/dealsoffreedom"
                ),

                InlineKeyboardButton(
                    "🔥 More Deals",
                    url="https://t.me/dealsoffreedom"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        # CLEAN MESSAGE
        message = """
🔥 HOT DEAL ALERT 🔥

💥 Limited Time Offer
⚡ Best Price Online

✅ Trending Product
✅ Fast Delivery
✅ Huge Discount Live

👇 Buy From Button Below 👇
"""

        # SEND MESSAGE
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=message,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )

        # SEND PRODUCT PREVIEW SEPARATELY
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
            "❌ Send Valid Shopping Product Link"
        )

# ==========================================
# MAIN
# ==========================================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link)
)

print("🚀 Deals Bot Running...")

app.run_polling()
