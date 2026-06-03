import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# एरर और लॉग्स देखने के लिए सेटअप
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Railway के Environment Variables से टोकन उठाना
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")

# 1. /start कमांड के लिए फंक्शन
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("हेलो भाई! मैं एक्टिव हूँ। अपना मैसेज भेजो, मैं Sarvam AI से प्रोसेस करके जवाब दूंगा।")

# 2. Sarvam AI API को कॉल करने का फंक्शन (Error 400 से बचने के लिए सही फॉर्मेट)
def call_sarvam_ai(user_text):
    # नोट: यह Sarvam AI के टेक्स्ट कंप्लीशन/ट्रांसलेशन का स्टैंडर्ड फॉर्मेट है
    # अगर आप उनका कोई विशिष्ट मॉडल (जैसे TTS/STT) यूज़ कर रहे हैं, तो URL उसके अनुसार बदलें
    url = "https://api.sarvam.ai/v1/chat/completions" 
    
    headers = {
        "api-subscription-key": SARVAM_API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "sarvam-2b", # या जो भी मॉडल आप यूज़ कर रहे हैं
        "messages": [
            {"role": "user", "content": user_text}
        ]
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            result = response.json()
            # Sarvam AI के रिस्पॉन्स से टेक्स्ट निकालना
            return result['choices'][0]['message']['content']
        else:
            logger.error(f"Sarvam AI Error {response.status_code}: {response.text}")
            return f"अरे यार, Sarvam AI की तरफ से एरर आया है (Code: {response.status_code})।"
    except Exception as e:
        logger.error(f"API Call Failed: {str(e)}")
        return "कनेक्शन में कुछ गड़बड़ी हुई है।"

# 3. आने वाले मैसेजेस को हैंडल करने का फंक्शन
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    # अगर खाली मैसेज है तो एरर 400 से बचने के लिए यहीं रोक दें
    if not user_text:
        return

    # बोट टाइप कर रहा है... ऐसा स्टेटस दिखाएं
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Sarvam AI से जवाब लाएं
    ai_response = call_sarvam_ai(user_text)
    
    # यूजर को जवाब भेजें
    await update.message.reply_text(ai_response)

# मुख्य फंक्शन जो बोट को स्टार्ट करेगा
def main():
    if not TELEGRAM_TOKEN or not SARVAM_API_KEY:
        logger.error("क्रिटिकल एरर: TELEGRAM_TOKEN या SARVAM_API_KEY सेट नहीं है!")
        return

    # बोट एप्लीकेशन बनाएं
    application = Application.builder().token(TELEGRAM_TOKEN).build()

    # कमांड और मैसेज हैंडलर्स जोड़ें
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # [IMPORTANT] drop_pending_updates=True लगाने से एरर 409 (Conflict) तुरंत खत्म हो जाएगा
    logger.info("बोट स्टार्ट हो रहा है और पुराने पेंडिंग मैसेजेस साफ़ किए जा रहे हैं...")
    application.run_polling(drop_pending_updates=True)

if __name__ == '__main__':
    main()
    
