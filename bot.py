import os

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# =========================
# CONFIG
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_ID = "@dealsoffreedom"

CHANNEL_LINK = "https://t.me/dealsoffreedom"

# =========================
# START COMMAND
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 Welcome To Deals Of Freedom 🔥\n\nSend Any Shopping Affiliate Link 🚀",
        reply_markup=ReplyKeyboardRemove()
    )

# =========================
# ABOUT COMMAND
# =========================

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🔥 Deals Of Freedom Bot

✅ Amazon Affiliate
✅ Flipkart Affiliate
✅ Myntra
✅ Ajio
✅ Nykaa
✅ Snapdeal

Auto Deal Posting Bot 🚀
"""

    await update.message.reply_text(text)

# =========================
# HANDLE LINKS
# =========================

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    original_link = update.message.text.strip()

    lower_link = original_link.lower()

    shopping_sites = [
        "amazon",
        "amzn.to",

        "flipkart",
        "fkrt.in",
        "fkrt.cc",
        "linkredirect.in",

        "myntra",
        "ajio",
        "nykaa",
        "snapdeal"
    ]

    # VALIDATE LINK
    if any(site in lower_link for site in shopping_sites):

        keyboard = [
            [
                InlineKeyboardButton(
                    "🛒 Buy Now",
                    url=original_link
                )
            ],
            [
                InlineKeyboardButton(
                    "📢 Join Channel",
                    url=CHANNEL_LINK
                ),
                InlineKeyboardButton(
                    "🔥 More Deals",
                    url=CHANNEL_LINK
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        message = f"""
🔥 HOT DEAL ALERT 🔥

⚡ Best Price Online
💥 Limited Time Offer

👇 Buy From Button Below 👇

{original_link}
"""

        try:

            await context.bot.send_message(
                chat_id=CHANNEL_ID,
                text=message,
                reply_markup=reply_markup,
                disable_web_page_preview=False
            )

            await update.message.reply_text(
                "✅ Deal Posted Successfully 🚀"
            )

        except Exception as e:

            await update.message.reply_text(
                f"❌ Error:\n{e}"
            )

    else:

        await update.message.reply_text(
            "❌ Send Valid Shopping Product Link"
        )

# =========================
# MAIN
# =========================

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("about", about))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_link
        )
    )

    print("Bot Running Successfully 🚀")

    app.run_polling()

# =========================

if __name__ == "__main__":
    main()
