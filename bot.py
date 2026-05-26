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

BOT_TOKEN = "YOUR_BOT_TOKEN"

CHANNEL_ID = "@dealsoffreedom"

CHANNEL_LINK = "https://t.me/dealsoffreedom"


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 Send Amazon Affiliate Link 🔥"
    )


# =========================
# MAIN FUNCTION
# =========================

async def post_deal(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    link = update.message.text.strip()

    if "amazon." not in link and "amzn." not in link:

        await update.message.reply_text(
            "❌ Send Valid Amazon Link"
        )

        return

    # =====================
    # BUTTONS
    # =====================

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

    # =====================
    # SEND ONLY LINK
    # AMAZON AUTO PREVIEW
    # =====================

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text=link,
        disable_web_page_preview=False
    )

    # =====================
    # SEND BUTTONS BELOW
    # =====================

    await context.bot.send_message(
        chat_id=CHANNEL_ID,
        text="""
🔥 HOT DEAL ALERT 🔥

💥 Best Price Online
⚡ Limited Time Offer
🚀 Hurry Up Before Stock Ends

👇 Buy From Button Below 👇
""",
        reply_markup=reply_markup
    )

    await update.message.reply_text(
        "✅ Deal Posted Successfully 🚀"
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
            post_deal
        )
    )

    print("Bot Running 🚀")

    app.run_polling()


if __name__ == "__main__":
    main()
