import os
import requests

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
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 Welcome To Deals Of Freedom 🔥\n\nSend Amazon Affiliate Link 🚀",
        reply_markup=ReplyKeyboardRemove()
    )

# =========================
# ABOUT
# =========================

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🔥 Deals Of Freedom Bot

✅ Amazon Affiliate Preview
✅ Auto Product Details
✅ Auto Product Image
✅ Buy Now Button
✅ Join Channel Button
✅ More Deals Button

🚀 Fully Automatic Deal Bot
"""

    await update.message.reply_text(text)

# =========================
# HANDLE AMAZON LINK
# =========================

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    original_link = update.message.text.strip()

    lower_link = original_link.lower()

    # =====================
    # VALIDATE AMAZON LINK
    # =====================

    if "amazon." not in lower_link and "amzn.to" not in lower_link:

        await update.message.reply_text(
            "❌ Send Valid Amazon Affiliate Link"
        )

        return

    # =====================
    # CLEAN LINK
    # KEEP AFFILIATE TAG
    # =====================

    clean_link = original_link

    if "&ref=" in clean_link:
        clean_link = clean_link.split("&ref=")[0]

    if "?ref=" in clean_link:
        clean_link = clean_link.split("?ref=")[0]

    # =====================
    # EXPAND SHORT LINK
    # =====================

    expanded_link = clean_link

    if "amzn.to" in clean_link:

        try:

            response = requests.get(
                clean_link,
                allow_redirects=True,
                timeout=10
            )

            expanded_link = response.url

        except:

            expanded_link = clean_link

    # =====================
    # BUTTONS
    # =====================

    keyboard = [

        [
            InlineKeyboardButton(
                "🛒 Buy Now",
                url=clean_link
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

    reply_markup = InlineKeyboardMarkup(
        keyboard
    )

    try:

        # =====================
        # SEND AMAZON PREVIEW
        # =====================

        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=expanded_link,
            disable_web_page_preview=False
        )

        # =====================
        # SEND BUTTONS
        # =====================

        await context.bot.send_message(
            chat_id=CHANNEL_ID,

            text="""
🔥 HOT DEAL ALERT 🔥

💥 Best Price Online
⚡ Limited Time Offer
🚀 Hurry Up Before Stock Ends

👇 Buy From Button Below 👇
""",

            reply_markup=reply_markup
        )

        await update.message.reply_text(
            "✅ Deal Posted Successfully 🚀"
        )

    except Exception as e:

        await update.message.reply_text(
            f"❌ Error:\n{e}"
        )

# =========================
# MAIN
# =========================

def main():

    app = Application.builder().token(
        BOT_TOKEN
    ).build()

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CommandHandler(
            "about",
            about
        )
    )

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
