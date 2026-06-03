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

# Railway से सिर्फ टेलीग्राम टोकन उठाना
TELEGRAM_TOKEN = os.getenv("8881399321:AAE4i95uFHxuJ-6Pj9AChP006shdTffWV58")

# ⚠️ यहाँ अपने चैनल का यूज़रनेम डालें (@ लगाना ज़रूरी है)
# उदाहरण: "@dealsoffreedom" या "@Deals_duniya_by_om" जो भी आपके चैनल का हैंडल हो
CHANNEL_USERNAME = "@dealsoffreedom" 

# /start कमांड
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"हेलो भाई! आपका डील्स बोट एक्टिव है।\n"
        f"अब आप मुझे जो भी प्रोडक्ट लिंक या डील भेजेंगे, मैं उसे सीधे आपके चैनल {CHANNEL_USERNAME} पर पोस्ट कर दूँगा!"
    )

# चैनल पर सीधे यूज़रनेम के ज़रिए पोस्ट करने का फंक्शन
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    if not user_text:
        return

    try:
        # यहाँ बोट चैनल ID की जगह सीधे चैनल के यूज़रनेम पर मैसेज भेज रहा है
        await context.bot.send_message(chat_id=CHANNEL_USERNAME, text=user_text)
        await update.message.reply_text("✅ डील सफलतापूर्वक चैनल पर शेयर कर दी गई है!")
    except Exception as e:
        logger.error(f"चैनल पर भेजने में एरर आया: {e}")
        await update.message.reply_text(
            f"❌ चैनल पर पोस्ट नहीं हो पाया।\n\n"
            f"चेक करें कि:\n"
            f"1. कोड में चैनल का यूज़रनेम ({CHANNEL_USERNAME}) सही है या नहीं।\n"
            f"2. बोट आपके चैनल में Admin बना है या नहीं।"
        )

def main():
    if not TELEGRAM_TOKEN:
        logger.error("क्रिटिकल एरर: TELEGRAM_TOKEN सेट नहीं है!")
        return

    application = Application.builder().token(TELEGRAM_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("यूज़रनेम आधारित डील्स बोट स्टार्ट हो रहा है...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
    
