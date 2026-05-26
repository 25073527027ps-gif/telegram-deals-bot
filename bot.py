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

# =========================
# START COMMAND
# =========================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
🔥 Welcome To Deals Of Freedom 🔥

Send Any Shopping Product Link 🚀

✅ Amazon Affiliate Direct Link
✅ EarnKaro / Flipkart Link
✅ Buy Now Button
"""

    await update.message.reply_text(text)


# =========================
# MAIN LINK HANDLER
# =========================
async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    link = update.message.text.strip()

    # =========================
    # BUTTONS
    # =========================
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
                url="https://t.me/dealsoffreedom"
            ),

            InlineKeyboardButton(
                "🔥 More Deals",
                url="https://t.me/dealsoffreedom"
            )
        ]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    # =========================
    # AMAZON LINKS
    # =========================
    if "amazon." in link:

        # Amazon preview automatically aayega
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=link,
            reply_markup=reply_markup,
            disable_web_page_preview=False
        )

    # =========================
    # FLIPKART / EARNKARO
    # =========================
    else:

        caption = f"""
🔥 HOT DEAL ALERT 🔥

🛍 Product:
Hot Deal Product

💥 Best Price Online
⚡ Limited Time Offer
🚀 Hurry Up Before Stock Ends

👇 Buy From Button Below 👇
"""

        # Flipkart / EarnKaro
        # Telegram preview automatically show karega
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=f"{caption}\n\n{link}",
            reply_markup=reply_markup,
            disable_web_page_preview=False
        )

    # SUCCESS MESSAGE
    await update.message.reply_text(
        "✅ Deal Posted Successfully 🚀"
    )


# =========================
# MAIN FUNCTION
# =========================
def main():

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_link
        )
    )

    print("Bot Running 🚀")

    app.run_polling()


# =========================
# RUN BOT
# =========================
if __name__ == "__main__":
    main()
