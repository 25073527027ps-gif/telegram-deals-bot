import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# एरर और लॉग्स देखने के लिए सेटअप
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Railway के Environment Variables से सिर्फ टेलीग्राम टोकन उठाना
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

# 1. /start कमांड के लिए फंक्शन
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "हेलो भाई! आपका नॉर्मल डील्स बोट अब पूरी तरह एक्टिव है।\n"
        "अब Sarvam AI हटा दिया गया है, इसलिए कोई एरर नहीं आएगा।\n"
        "आप जो भी मैसेज या लिंक भेजेंगे, मैं उसे तुरंत प्रोसेस करूँगा!"
    )

# 2. नॉर्मल मैसेज हैंडलर (बिना AI के सीधा रिपॉन्स या फॉरवर्ड करने के लिए)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    if not user_text:
        return

    # यहाँ बोट बिना किसी AI के सीधे आपके मैसेज का जवाब देगा या उसे आगे प्रोसेस करेगा
    # उदाहरण के लिए: यह आपके भेजे गए मैसेज को ही वापस रिपीट कर रहा है (या आप इसे चैनल में फॉरवर्ड करा सकते हैं)
    reply_text = f"प्राप्त हुआ संदेश:\n\n{user_text}"
    
    await update.message.reply_text(reply_text)

# मुख्य फंक्शन जो बोट को स्टार्ट करेगा
def main():
    if not TELEGRAM_TOKEN:
        logger.error("क्रिटिकल एरर: TELEGRAM_TOKEN सेट नहीं है!")
        return

    # बोट एप्लीकेशन बनाएं
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # कमांड और मैसेज हैंडलर्स जोड़ें
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # पुराने पेंडिंग मैसेजेस साफ़ करने के लिए drop_pending_updates=True
    logger.info("नॉर्मल बोट स्टार्ट हो रहा है...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
    
