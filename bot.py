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
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🔥 Welcome To Deals Of Freedom 🔥

Send Amazon Affiliate Product Link 🚀
"""

    await update.message.reply_text(
        text,
        reply_markup=ReplyKeyboardRemove()
    )

# =========================
# ABOUT
# =========================

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🔥 Deals Of Freedom Bot

✅ Amazon Affiliate Support
✅ Auto Deal Posting
✅ Buy Now Buttons
✅ Professional Deal Format

🚀 Bot Running Successfully
"""

    await update.message.reply_text(text)

# =========================
# EXTRACT PRODUCT NAME
# =========================

def get_product_name(link):

    try:

        # Amazon link name extract
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

    original_link = update.message.text.strip()

    lower_link = original_link.lower()

    # =====================
    # VALIDATION
    # =====================

    if "amazon." not in lower_link and "amzn.to" not in lower_link:

        await update.message.reply_text(
            "❌ Send Valid Amazon Affiliate Link"
        )

        return

    # =====================
    # PRODUCT NAME
    # =====================

    product_name = get_product_name(original_link)

    # =====================
    # BUTTONS
    # =====================

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

    # =====================
    # MESSAGE
    # =====================

    message = f"""
🔥 HOT DEAL ALERT 🔥

🛍 Product:
{product_name}

💥 Best Price Online
⚡ Limited Time Offer
🚀 Hurry Up Before Stock Ends

👇 Buy From Button Below 👇
"""

    # =====================
    # SEND TO CHANNEL
    # =====================

    try:

        # First send affiliate link separately
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=original_link,
            disable_web_page_preview=False
        )

        # Then send formatted deal
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=message,
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
        CommandHandler("about", about)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_link
        )
    )

    print("🚀 Bot Running Successfully")

    app.run_polling()

# =========================

if __name__ == "__main__":
    main()
