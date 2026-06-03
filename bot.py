import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# लॉग्स सेटअप
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Railway से Variables उठाना
TELEGRAM_TOKEN = os.getenv("8881399321:AAE4i95uFHxuJ-6Pj9AChP006shdTffWV58")
CHANNEL_ID = os.getenv("dealsoffreedom")  # आपके चैनल की ID (जैसे: -100xxxxxxxxx)

# /start कमांड
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "हेलो भाई! आपका डील्स बोट एक्टिव है।\n"
        "अब आप मुझे जो भी प्रोडक्ट लिंक या डील भेजेंगे, मैं उसे सीधे आपके चैनल पर पोस्ट कर दूँगा!"
    )

# चैनल पर प्रोडक्ट/लिंक शेयर करने का फंक्शन
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    if not user_text:
        return

    if not CHANNEL_ID:
        await update.message.reply_text("❌ एरर: Railway में CHANNEL_ID सेट नहीं की गई है!")
        return

    try:
        # जो भी आप बोट को भेजेंगे, बोट उसे सीधे आपके चैनल पर भेज देगा
        await context.bot.send_message(chat_id=CHANNEL_ID, text=user_text)
        await update.message.reply_text("✅ डील सफलतापूर्वक चैनल पर शेयर कर दी गई है!")
    except Exception as e:
        logger.error(f"चैनल पर भेजने में एरर आया: {e}")
        await update.message.reply_text(f"❌ चैनल पर पोस्ट नहीं हो पाया। एरर: {e}\n(चेक करें कि बोट चैनल में एडमिन है या नहीं)")

def main():
    if not TELEGRAM_TOKEN:
        logger.error("क्रिटिकल एरर: TELEGRAM_TOKEN सेट नहीं है!")
        return

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("चैनल डील्स बोट स्टार्ट हो रहा है...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
    
