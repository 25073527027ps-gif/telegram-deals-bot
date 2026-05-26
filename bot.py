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

BOT_TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_ID = "@dealsoffreedom"

CHANNEL_LINK = "https://t.me/dealsoffreedom"

# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "Send:\n\n1st Line = Short Affiliate Link\n2nd Line = Long Amazon Link",
        reply_markup=ReplyKeyboardRemove()
    )

# =========================
# PRODUCT NAME
# =========================

def get_product_name(link):

    try:

        if "/dp/" in link:

            name = link.split("/dp/")[0]

            name = name.split("/")[-1]

            name = name.replace("-", " ")

            return name.title()

        return "Hot Deal Product"

    except:

        return "Hot Deal Product"

# =========================
# HANDLE LINK
# =========================

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip()

    lines = text.split("\n")

    if len(lines) < 2:

        await update.message.reply_text(
            "❌ Send 2 Links"
        )

        return

    short_link = lines[0].strip()

    long_link = lines[1].strip()

    product_name = get_product_name(long_link)

    keyboard = [

        [
            InlineKeyboardButton(
                "🛒 Buy Now",
                url=short_link
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

    # =====================
    # STEP 1
    # SEND LONG LINK FOR PREVIEW
    # =====================

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=long_link,
        disable_web_page_preview=False
    )

    # =====================
    # STEP 2
    # SEND DEAL MESSAGE
    # =====================

    message = f"""
🔥 HOT DEAL ALERT 🔥

🛍 Product:
{product_name}

💥 Best Price Online
⚡ Limited Time Offer
🚀 Hurry Up Before Stock Ends

👇 Buy From Button Below 👇

🔗 {short_link}
"""

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=message,
        reply_markup=reply_markup
    )

    await update.message.reply_text(
        "✅ Deal Posted Successfully 🚀"
    )

# =========================
# MAIN
# =========================

def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_link
        )
    )

    print("Bot Running 🚀")

    app.run_polling()

# =========================

if __name__ == "__main__":
    main()
