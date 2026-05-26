import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("BOT_TOKEN")

keyboard = [
    ["📷 Send Photo"],
    ["🛒 Buy Now"],
    ["🔗 Affiliate Link"],
    ["ℹ️ About Bot"]
]

reply_markup = ReplyKeyboardMarkup(
    keyboard,
    resize_keyboard=True
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 Welcome To My Bot!",
        reply_markup=reply_markup
    )

async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "📷 Send Photo":
        await update.message.reply_text("📸 Please send your photo")

    elif text == "🛒 Buy Now":
        await update.message.reply_text(
            "🛍️ Buy Here:\nhttps://amzn.to/YOUR_LINK"
        )

    elif text == "🔗 Affiliate Link":
        await update.message.reply_text(
            "🔗 Your Affiliate Link:\nhttps://amzn.to/YOUR_LINK"
        )

    elif text == "ℹ️ About Bot":
        await update.message.reply_text(
            "🤖 This is Affiliate Deals Bot"
        )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, buttons))

print("Bot is running...")

app.run_polling()
