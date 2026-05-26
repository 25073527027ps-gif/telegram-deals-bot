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

# =====================================
# CONFIG
# =====================================

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_USERNAME = "@dealsoffreedom"

CHANNEL_LINK = "https://t.me/dealsoffreedom"


# =====================================
# START COMMAND
# =====================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🔥 Welcome To Deals Of Freedom 🔥

Send Product Links 🚀


✅ AMAZON

Send Direct Amazon Affiliate Link

Example:
https://amzn.in/xxxxx


✅ FLIPKART / EARNKARO

Format:

ORIGINAL: https://flipkart.com/product....

AFFILIATE: https://fkrt.cc/xxxxx
"""

    await update.message.reply_text(text)


# =====================================
# GET PRODUCT DETAILS
# =====================================

def get_product_details(url):

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Linux; Android 10; Mobile) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9"
    }

    try:

        # =========================
        # AMAZON SHORT LINK FIX
        # =========================

        if "amzn.in" in url:

            expanded = requests.get(
                url,
                headers=headers,
                allow_redirects=True,
                timeout=10
            )

            url = expanded.url

        # =========================
        # MAIN REQUEST
        # =========================

        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        soup = BeautifulSoup(
            response.text,
            "html.parser"
        )

        title = "Hot Deal Product"

        image = None

        # =========================
        # TITLE
        # =========================

        title_tag = soup.find(
            "meta",
            attrs={"property": "og:title"}
        )

        if title_tag:

            title = title_tag.get(
                "content"
            )

        # =========================
        # IMAGE
        # =========================

        image_tag = soup.find(
            "meta",
            attrs={"property": "og:image"}
        )

        if image_tag:

            image = image_tag.get(
                "content"
            )

        return title[:120], image

    except Exception as e:

        print(e)

        return "Hot Deal Product", None


# =====================================
# MESSAGE HANDLER
# =====================================

async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    text = update.message.text.strip()

    original_link = None
    affiliate_link = None

    # =====================================
    # AMAZON DIRECT
    # =====================================

    if "amazon." in text or "amzn." in text:

        original_link = text

        affiliate_link = text

    # =====================================
    # FLIPKART FORMAT
    # =====================================

    elif (
        "ORIGINAL:" in text
        and
        "AFFILIATE:" in text
    ):

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
                "❌ Wrong Format"
            )

            return

    else:

        await update.message.reply_text(
            "❌ Wrong Format\n\n"
            "Amazon → Direct Link\n\n"
            "Flipkart Format:\n\n"
            "ORIGINAL: https://flipkart.com/...\n\n"
            "AFFILIATE: https://fkrt.cc/..."
        )

        return

    # =====================================
    # PRODUCT DETAILS
    # =====================================

    title, image = get_product_details(
        original_link
    )

    # =====================================
    # CAPTION
    # =====================================

    caption = f"""
🔥 HOT DEAL ALERT 🔥

🛍 Product:
{title}

💥 Best Price Online
⚡ Limited Time Offer
🚀 Hurry Up Before Stock Ends

👇 Buy From Button Below 👇
"""

    # =====================================
    # BUTTONS
    # =====================================

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

    # =====================================
    # SEND POST
    # =====================================

    try:

        # SEND PHOTO POST
        if (
            image
            and
            image.startswith("http")
        ):

            await context.bot.send_photo(
                chat_id=CHANNEL_USERNAME,
                photo=image,
                caption=caption,
                reply_markup=reply_markup
            )

        # FALLBACK TEXT POST
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

        # FALLBACK IF PHOTO FAILS
        try:

            await context.bot.send_message(
                chat_id=CHANNEL_USERNAME,
                text=caption,
                reply_markup=reply_markup
            )

            await update.message.reply_text(
                "✅ Deal Posted Successfully 🚀"
            )

        except Exception as err:

            await update.message.reply_text(
                f"❌ Error:\n{err}"
            )


# =====================================
# MAIN
# =====================================

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
