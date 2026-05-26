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

Send Message Like This 👇

SHORT LINK
LONG AMAZON LINK
"""

    await update.message.reply_text(
        text,
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
# HANDLE MESSAGE
# =========================

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text.strip()

    lines = text.split("\n")

    # =====================
    # REQUIRE 2 LINKS
    # =====================

    if len(lines) < 2:

        await update.message.reply_text(
            "❌ Send:\n\nSHORT LINK\nLONG AMAZON LINK"
        )

        return

    short_link = lines[0].strip()

    long_link = lines[1].strip()

    # =====================
    # VALIDATE
    # =====================

    if "amzn.to" not in short_link.lower():

        await update.message.reply_text(
            "❌ First Link Must Be Short Amazon Link"
        )

        return

    if "amazon." not in long_link.lower():

        await update.message.reply_text(
            "❌ Second Link Must Be Full Amazon Product Link"
        )

        return

    # =====================
    # PRODUCT NAME
    # =====================

    product_name = get_product_name(long_link)

    # =====================
    # BUTTONS
    # =====================

    keyboard = [

        [
            InlineKeyboardButton(
                "🛒 Buy Now",
                url=long_link
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
{short_link}

🔥 HOT DEAL ALERT 🔥

🛍 Product:
{product_name}

💥 Best Price Online
⚡ Limited Time Offer
🚀 Hurry Up Before Stock Ends

👇 Buy From Button Below 👇
"""

    # =====================
    # SEND
    # =====================

    try:

        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=message,
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

# =========================
# ABOUT
# =========================

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🔥 Deals Of Freedom Bot

✅ Short Link Visible
✅ Product Preview Working
✅ Buy Button
✅ Professional Deal Layout
"""

    await update.message.reply_text(text)

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

    print("🚀 Bot Running Successfully")

    app.run_polling()

# =========================

if __name__ == "__main__":
    main()
