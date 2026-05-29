import re
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# लॉगिंग सेट कर रहे हैं ताकि रेलवे लॉग्स में एरर साफ़ दिखे
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# 1. अपनी डिटेल्स यहाँ भरें
BOT_TOKEN = "8601951285:AAE09-x_4Peuh3WSJN68U21iGFKsCuVnLLE"          # अपना बोट टोकन डालें
TARGET_CHANNEL = "@dealsoffreedom"             # आपके चैनल का यूजरनेम (@ के साथ)
CHANNEL_LINK = "https://t.me/dealsoffreedom"      # चैनल का इनवाइट लिंक
MORE_DEALS_LINK = "https://t.me/dealsoffreedom"

# एफिलिएट ट्रैकिंग आईडी
AMAZON_TAG = "your_amazon_tag-21"
FLIPKART_AFF_ID = "your_flipkart_id"

def modify_link(original_url):
    """लिंक्स को एफिलिएट लिंक में बदलना"""
    if "amazon.in" in original_url or "amzn.to" in original_url:
        clean_url = re.sub(r'tag=[^&]+', '', original_url)
        connector = "&" if "?" in clean_url else "?"
        return f"{clean_url.strip()}{connector}tag={AMAZON_TAG}"

    elif "flipkart.com" in original_url:
        connector = "&" if "?" in original_url else "?"
        return f"{original_url.strip()}{connector}affid={FLIPKART_AFF_ID}"

    return original_url.strip()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text:
        return

    # मैसेज में से लिंक्स ढूंढना
    urls = re.findall(r'(https?://[^\s]+)', text)
    
    if urls:
        # पहले लिंक को 'Buy Now' बटन के लिए सेट करें
        buy_now_url = modify_link(urls[0])
        
        # पूरे टेक्स्ट में सभी लिंक्स को रिप्लेस करना
        modified_text = text
        for url in urls:
            new_url = modify_link(url)
            modified_text = modified_text.replace(url, new_url)
        
        # 🌟 HTML फॉर्मेट में आकर्षक हेडिंग
        final_message_text = f"🔥 <b>NEW BLAST DEAL</b> 🔥\n\n{modified_text}"
        
        # 🔘 नीचे सुंदर इनलाइन बटन्स
        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now (खरीदें)", url=buy_now_url)],
            [
                InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK),
                InlineKeyboardButton("🛍️ More Deals", url=MORE_DEALS_LINK)
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        try:
            # चैनल पर पोस्ट भेजना
            await context.bot.send_message(
                chat_id=TARGET_CHANNEL, 
                text=final_message_text, 
                reply_markup=reply_markup,
                parse_mode="HTML"  # सुरक्षित फॉर्मेटिंग
            )
            await update.message.reply_text("✅ डील बटन्स के साथ चैनल पर पोस्ट हो गई है!")
        except Exception as e:
            # अगर टेलीग्राम कोई एरर देता है तो आपको चैट में पता चल जाएगा
            await update.message.reply_text(f"❌ चैनल पर पोस्ट नहीं हुई। एरर: {e}")

if __name__ == '__main__':
    # पूरी तरह से न्यू वर्शन (v20+) एसिंक्रोनस सेटअप
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # टेक्स्ट मैसेज हैंडलर
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("बॉट सफलताबाूर्वक चालू हो गया है...")
    app.run_polling()
