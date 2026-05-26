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
        "🔥 Welcome To Deals Of Freedom 🔥\n\nSend Any Shopping Product Link 🚀",
        reply_markup=ReplyKeyboardRemove()
    )

# =========================
# ABOUT COMMAND
# =========================

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🔥 Deals Of Freedom Bot

✅ Amazon
✅ Flipkart
✅ Myntra
✅ Ajio
✅ Nykaa
✅ Snapdeal

Product links automatically channel par post honge 🚀
"""

    await update.message.reply_text(text)

# =========================
# HANDLE PRODUCT LINKS
# =========================

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    link = update.message.text.strip().lower()

    shopping_sites = [
        "amazon",
        "amzn.to",
        "flipkart",
        "fkrt.in",
        "myntra",
        "ajio",
        "nykaa",
        "snapdeal"
    ]

    if any(site in link for site in shopping_sites):

        keyboard = [
            [
                InlineKeyboardButton(
                    "🛒 Buy Now",
                    url=update.message.text.strip()
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

        text = f"""
🔥 HOT DEAL ALERT 🔥

⚡ Best Price Online
💥 Limited Time Offer

👇 Buy From Button Below 👇

{update.message.text.strip()}
"""

        try:

            await context.bot.send_message(
                chat_id=CHANNEL_ID,
                text=text,
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

    print("Bot Running Successfully...")

    app.run_polling()

# =========================

if __name__ == "__main__":
    main()
