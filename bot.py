import os
import re
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


# START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
🔥 Welcome To Deals Of Freedom 🔥

Send Shopping Product Link 🚀

Amazon → Direct Link
Flipkart → Use Format:

ORIGINAL: original product link
AFFILIATE: earnkaro/fkrt link
"""
    await update.message.reply_text(text)


# SCRAPE PRODUCT DETAILS
def get_product_details(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        title = "Hot Deal Product"
        image = None

        # AMAZON
        amazon_title = soup.find(id="productTitle")
        if amazon_title:
            title = amazon_title.get_text(strip=True)

        amazon_img = soup.find(id="landingImage")
        if amazon_img:
            image = amazon_img.get("src")

        # FLIPKART
        if "flipkart" in url:

            meta_title = soup.find("meta", property="og:title")
            if meta_title:
                title = meta_title.get("content")

            meta_img = soup.find("meta", property="og:image")
            if meta_img:
                image = meta_img.get("content")

        return title[:100], image

    except:
        return "Hot Deal Product", None


# MAIN MESSAGE HANDLER
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip()

    original_link = None
    affiliate_link = None

    # AMAZON DIRECT
    if "amazon." in text or "amzn." in text:
        original_link = text
        affiliate_link = text

    # FLIPKART FORMAT
    elif "ORIGINAL:" in text and "AFFILIATE:" in text:

        try:
            original_link = text.split(
                "ORIGINAL:"
            )[1].split(
                "AFFILIATE:"
            )[0].strip()

            affiliate_link = text.split(
                "AFFILIATE:"
            )[1].strip()

        except:
            pass

    else:
        await update.message.reply_text(
            "❌ Wrong Format\n\n"
            "Amazon → Direct Link\n\n"
            "Flipkart Format:\n\n"
            "ORIGINAL: https://flipkart....\n"
            "AFFILIATE: https://fkrt...."
        )
        return

    # PRODUCT DETAILS
    title, image = get_product_details(original_link)

    caption = f"""
🔥 HOT DEAL ALERT 🔥

🛍 Product:
{title}

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
                url="https://t.me/dealsoffreedom"
            ),
            InlineKeyboardButton(
                "🔥 More Deals",
                url="https://t.me/dealsoffreedom"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # SEND TO CHANNEL
    try:

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
        await update.message.reply_text(
            f"❌ Error:\n{e}"
        )


# MAIN
def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

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
