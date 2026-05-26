import os
import requests

from bs4 import BeautifulSoup

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_USERNAME = "@dealsoffreedom"
CHANNEL_LINK = "https://t.me/dealsoffreedom"


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 Send Original + Affiliate Link"
    )


# =========================
# GET PRODUCT DATA
# =========================

def get_product_data(url):

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(
        url,
        headers=headers,
        timeout=20
    )

    soup = BeautifulSoup(
        response.text,
        "html.parser"
    )

    title = "🔥 HOT DEAL ALERT 🔥"
    image = None

    # TITLE

    title_tag = soup.find(
        "meta",
        property="og:title"
    )

    if title_tag:
        title = title_tag.get("content")

    # IMAGE

    image_tag = soup.find(
        "meta",
        property="og:image"
    )

    if image_tag:
        image = image_tag.get("content")

    return title, image


# =========================
# HANDLE MESSAGE
# =========================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if not text:
        return

    try:

        lines = text.splitlines()

        original_link = ""
        affiliate_link = ""

        for line in lines:

            if "ORIGINAL:" in line:
                original_link = line.replace(
                    "ORIGINAL:",
                    ""
                ).strip()

            if "AFFILIATE:" in line:
                affiliate_link = line.replace(
                    "AFFILIATE:",
                    ""
                ).strip()

        if not original_link or not affiliate_link:

            await update.message.reply_text(
                "❌ Format Wrong"
            )
            return

        # GET PRODUCT DETAILS

        title, image = get_product_data(
            original_link
        )

        caption = f"""
🔥 HOT DEAL ALERT 🔥

🛍 Product:
{title[:120]}

💥 Best Price Online
⚡ Limited Time Offer
🚀 Hurry Up Before Stock Ends

👇 Buy From Button Below 👇
"""

        # BUTTONS

        keyboard = [
            [
                InlineKeyboardButton(
                    "🛒 Buy Now",
                    url=affiliate_link
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

        # SEND POST

        if image:

            await context.bot.send_photo(
                chat_id=CHANNEL_USERNAME,
                photo=image,
                caption=caption,
                reply_markup=reply_markup
            )

        else:

            await context.bot.send_message(
                chat_id=CHANNEL_USERNAME,
                text=caption,
                reply_markup=reply_markup
            )

        await update.message.reply_text(
            "✅ Deal Posted Successfully 🚀"
        )

    except Exception as e:

        print(e)

        await update.message.reply_text(
            "❌ Error"
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
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message
        )
    )

    print("Bot Running...")

    app.run_polling()


if __name__ == "__main__":
    main()
