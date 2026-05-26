import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# =========================================
# BOT SETTINGS
# =========================================

TOKEN = os.getenv("BOT_TOKEN")

CHANNEL_ID = "@dealsoffreedom"

# =========================================
# START COMMAND
# =========================================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    await update.message.reply_text(
        "🔥 Send Any Amazon Affiliate Link 🔥"
    )

# =========================================
# HANDLE AMAZON LINKS
# =========================================

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    link = update.message.text.strip()

    # AMAZON LINK CHECK
    if "amazon" in link or "amzn.to" in link:

        # ATTRACTIVE DEAL MESSAGE
        message = f"""
🔥 MEGA DEAL ALERT 🔥

🛒 Best Product Available
💥 Huge Discount Live
⚡ Limited Time Offer

━━━━━━━━━━━━━━━

✅ Trusted Amazon Product
✅ Fast Delivery
✅ Best Online Price

👉 Buy Now:
{link}

━━━━━━━━━━━━━━━

⚠️ Hurry Before Price Increase
📢 Join: https://t.me/dealsoffreedom
"""

        # SEND TO CHANNEL
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=message,
            disable_web_page_preview=False
        )

        # SUCCESS REPLY
        await update.message.reply_text(
            "✅ Deal Posted To Channel Successfully 🚀"
        )

    else:

        await update.message.reply_text(
            "❌ Please Send Valid Amazon Affiliate Link"
        )

# =========================================
# MAIN BOT
# =========================================

app = ApplicationBuilder().token(TOKEN).build()

# COMMANDS
app.add_handler(CommandHandler("start", start))

# MESSAGE HANDLER
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link)
)

# =========================================
# RUN BOT
# =========================================

print("🚀 Amazon Deals Bot Running...")

app.run_polling()
