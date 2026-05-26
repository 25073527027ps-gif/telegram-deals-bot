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

Send Product Link 🚀

✅ Amazon:
Send Direct Amazon Affiliate Link

Example:
https://amzn.in/xxxxx


✅ Flipkart / EarnKaro:

Format:

ORIGINAL: original product link
AFFILIATE: affiliate link
"""

    await update.message.reply_text(text)


# =========================
# SCRAPE PRODUCT DETAILS
# =========================

def get_product_details(url):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 10; Mobile) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Mobile Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        soup = BeautifulSoup(response.text, "html.parser")

        title = "Hot Deal Product"
        image = None

        # AMAZON
        if "amazon" in url or "amzn" in url:

            title_tag = soup.find(
                "meta",
                attrs={"property": "og:title"}
            )

            if title_tag:
                title = title_tag.get("content")

            image_tag = soup.find(
                "meta",
                attrs={"property": "og:image"}
            )

            if image_tag:
                image = image_tag.get("content")

        # FLIPKART
        elif "flipkart" in url:

            title_tag = soup.find(
                "meta",
                attrs={"property": "og:title"}
            )

            if title_tag:
                title = title_tag.get("content")

            image_tag = soup.find(
                "meta",
                attrs={"property": "og:image"}
            )

            if image_tag:
                image = image_tag.get("content")

        return title[:120], image

    except Exception as e:
        print(e)
        return "Hot Deal Product", None


# =========================
# MAIN MESSAGE HANDLER
# =========================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip()

    original_link = None
    affiliate_link = None

    # =========================
    # AMAZON DIRECT
    # =========================

    if "amazon." in text or "amzn." in text:

        original_link = text
        affiliate_link = text

    # =========================
    # FLIPKART FORMAT
    # =========================

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

            await update.message.reply_text(
                "❌ Format Wrong"
            )
            return

    else:

        await update.message.reply_text(
            "❌ Wrong Format\n\n"
            "Amazon → Direct Link\n\n"
            "Flipkart Format:\n\n"
            "ORIGINAL: https://flipkart.com/...\n"
            "AFFILIATE: https://fkrt.cc/..."
        )

        return

    # =========================
    # GET PRODUCT DETAILS
    # =========================

    title, image = get_product_details(original_link)

    # =========================
    # CAPTION
    # =========================

    caption = f"""
🔥 HOT DEAL ALERT 🔥

🛍 Product:
{title}

💥 Best Price Online
⚡ Limited Time Offer
🚀 Hurry Up Before Stock Ends

👇 Buy From Button Below 👇
"""

    # =========================
    # BUTTONS
    # =========================

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

    reply_markup = InlineKeyboardMarkup(keyboard)

    # =========================
    # SEND TO CHANNEL
    # =========================

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
