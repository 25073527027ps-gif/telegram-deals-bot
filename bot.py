import os
import re
import requests
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

# =========================
# CONFIG
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_USERNAME = "@dealsoffreedom"
CHANNEL_LINK = "https://t.me/dealsoffreedom"

# =========================
# START COMMAND
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🔥 Welcome To Deals Of Freedom 🔥

Send Any Shopping Product Link 🚀
"""

    await update.message.reply_text(text)


# =========================
# EXTRACT IMAGE
# =========================

def get_image_from_html(html):

    patterns = [
        r'<meta property="og:image" content="(.*?)"',
        r'<meta name="twitter:image" content="(.*?)"',
        r'"image":"(.*?)"',
    ]

    for pattern in patterns:
        match = re.search(pattern, html)

        if match:
            return match.group(1).replace("\\u002F", "/")

    return None


# =========================
# EXTRACT TITLE
# =========================

def get_title_from_html(html):

    patterns = [
        r'<meta property="og:title" content="(.*?)"',
        r'<title>(.*?)</title>',
    ]

    for pattern in patterns:
        match = re.search(pattern, html)

        if match:
            return match.group(1)

    return "🔥 HOT DEAL ALERT 🔥"


# =========================
# HANDLE LINKS
# =========================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if not text:
        return

    original_link = text.strip()
    lower_link = original_link.lower()

    # ACCEPT ALL LINKS
    if "http" not in lower_link:

        await update.message.reply_text(
            "❌ Send Valid Shopping Product Link"
        )
        return

    try:

        headers = {
            "User-Agent": (
                "Mozilla/5.0"
            )
        }

        response = requests.get(
            original_link,
            headers=headers,
            timeout=15
        )

        html = response.text

        title = get_title_from_html(html)
        image_url = get_image_from_html(html)

        caption = f"""
🔥 HOT DEAL ALERT 🔥

✨ {title[:120]}

💥 Best Price Online
⚡ Limited Time Offer
🛒 Grab Fast Before Price Increase

👇 Buy From Button Below 👇
"""

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

        # SEND TO CHANNEL

        if image_url:

            await context.bot.send_photo(
                chat_id=CHANNEL_USERNAME,
                photo=image_url,
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
            "❌ Error While Posting Deal"
        )


# =========================
# MAIN
# =========================

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
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
