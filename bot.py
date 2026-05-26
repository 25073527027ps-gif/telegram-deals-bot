import os
import re
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
✅ Meesho

Product links automatically channel par post honge 🚀
"""

    await update.message.reply_text(text)

# =========================
# EXTRACT IMAGE
# =========================

def get_product_image(url):

    try:

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        html = requests.get(url, headers=headers).text

        image = re.search(
            r'<meta property="og:image" content="(.*?)"',
            html
        )

        if image:
            return image.group(1)

    except:
        pass

    return None

# =========================
# HANDLE PRODUCT LINKS
# =========================

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    link = update.message.text.strip()

    shopping_sites = [
        "amazon",
        "flipkart",
        "myntra",
        "ajio",
        "meesho",
        "nykaa",
        "snapdeal"
    ]

    if any(site in link.lower() for site in shopping_sites):

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
                    url=CHANNEL_LINK
                ),
                InlineKeyboardButton(
                    "🔥 More Deals",
                    url=CHANNEL_LINK
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        caption = f"""
🔥 HOT DEAL ALERT 🔥

⚡ Best Price Online
💥 Limited Time Offer

👇 Buy From Button Below 👇
"""

        image_url = get_product_image(link)

        try:

            if image_url:

                await context.bot.send_photo(
                    chat_id=CHANNEL_ID,
                    photo=image_url,
                    caption=caption,
                    reply_markup=reply_markup
                )

            else:

                await context.bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=caption,
                    reply_markup=reply_markup
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
