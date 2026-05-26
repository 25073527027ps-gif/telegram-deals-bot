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
# START
# ==========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 Send Amazon Affiliate Link 🔥"
    )

# ==========================================
# HANDLE AMAZON LINKS
# ==========================================

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    link = update.message.text.strip()

    if "amazon" in link or "amzn.to" in link:

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

        # DEAL MESSAGE
        message = f"""
🔥 HOT AMAZON DEAL 🔥

💥 Limited Time Offer
⚡ Best Price Available

✅ Fast Delivery
✅ Trusted Product
✅ Amazon Special Deal

👇 Product Link Below 👇

{link}
"""

        # SEND MESSAGE WITH BUTTONS
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=message,
            reply_markup=reply_markup,
            disable_web_page_preview=False
        )

        await update.message.reply_text(
            "✅ Deal Posted Successfully 🚀"
        )

    else:

        await update.message.reply_text(
            "❌ Please Send Valid Amazon Link"
        )

# ==========================================
# MAIN
# ==========================================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link)
)

print("🚀 Amazon Deals Bot Running...")

app.run_polling()
