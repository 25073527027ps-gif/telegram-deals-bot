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

# ==============================
# CONFIG
# ==============================

BOT_TOKEN = "YOUR_BOT_TOKEN"

CHANNEL_ID = "@dealsoffreedom"

CHANNEL_LINK = "https://t.me/dealsoffreedom"


# ==============================
# START COMMAND
# ==============================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🔥 Welcome To Deals Of Freedom 🔥

✅ Send Amazon Affiliate Link
✅ Automatic Product Preview
✅ Buy Now Button
✅ Professional Deal Post

🚀 Example:

https://amzn.in/xxxxx
"""

    await update.message.reply_text(text)


# ==============================
# AMAZON LINK HANDLER
# ==============================

async def amazon_post(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    link = update.message.text.strip()

    # ==========================
    # ONLY AMAZON LINKS ALLOWED
    # ==========================

    if (
        "amazon." not in link
        and
        "amzn." not in link
    ):

        await update.message.reply_text(
            "❌ Only Amazon Affiliate Links Allowed"
        )

        return

    # ==========================
    # BUTTONS
    # ==========================

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

    reply_markup = InlineKeyboardMarkup(
        keyboard
    )

    # ==========================
    # PROFESSIONAL CAPTION
    # ==========================

    text = f"""
🔥 HOT DEAL ALERT 🔥

💥 Best Price Online
⚡ Limited Time Offer
🚀 Hurry Up Before Stock Ends

👇 Buy From Button Below 👇

{link}
"""

    # ==========================
    # SEND TO CHANNEL
    # ==========================

    try:

        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=text,
            reply_markup=reply_markup,
            disable_web_page_preview=False
        )

        await update.message.reply_text(
            "✅ Amazon Deal Posted Successfully 🚀"
        )

    except Exception as e:

        await update.message.reply_text(
            f"❌ Error:\n{e}"
        )


# ==============================
# MAIN FUNCTION
# ==============================

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
            amazon_post
        )
    )

    print("Bot Running 🚀")

    app.run_polling()


# ==============================
# RUN
# ==============================

if __name__ == "__main__":
    main()
