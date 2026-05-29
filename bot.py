import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# 1. अपनी डिटेल्स यहाँ भरें
BOT_TOKEN = "8601951285:AAE09-x_4Peuh3WSJN68U21iGFKsCuVnLLE"      # अपना बोट टोकन डालें
TARGET_CHANNEL = "@dealsoffreedom"         # आपके चैनल का यूजरनेम (@ के साथ)
CHANNEL_LINK = "https://t.me/dealsoffreedom"  # चैनल का लिंक
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

def handle_message(update: Update, context: CallbackContext):
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
        
        # 🌟 HTML फॉर्मेट में आकर्षक हेडिंग जोड़ना (यह कभी एरर नहीं देगा)
        final_message_text = f"🔥 <b>NEW BLAST DEAL</b> 🔥\n\n{modified_text}"
        
        # 🔘 नीचे सुंदर इनलाइन बटन्स जोड़ना
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
            context.bot.send_message(
                chat_id=TARGET_CHANNEL, 
                text=final_message_text, 
                reply_markup=reply_markup,
                parse_mode="HTML"  # सुरक्षित और बेहतर फॉर्मेटिंग के लिए HTML का इस्तेमाल
            )
            # आपको बोट में कन्फर्मेशन मिलना
            update.message.reply_text("✅ डील बटन्स और न्यू अपडेट के साथ चैनल पर सफलतापूर्वक पोस्ट हो गई है!")
        except Exception as e:
            # अगर कोई गड़बड़ हो तो आपको चैट में एरर दिख जाएगा
            update.message.reply_text(f"❌ पोस्ट भेजने में एरर आया: {e}")

def main():
    # पुराने और नए दोनों टेलीग्राम लाइब्रेरी वर्शन्स के लिए कम्पैटिबल सेटअप
    try:
        # अगर आपका python-telegram-bot वर्शन पुराना है
        updater = Updater(BOT_TOKEN, use_context=True)
        dp = updater.dispatcher
        dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
        print("बॉट चालू हो गया है (वर्मन 13)...")
        updater.start_polling()
        updater.idle()
    except Exception:
        # अगर आपका वर्शन नया (v20+) है तो यह तरीका काम करेगा
        from telegram.ext import ApplicationBuilder
        app = ApplicationBuilder().token(BOT_TOKEN).build()
        from telegram.ext import MessageHandler as NewMessageHandler
        from telegram.ext import filters as new_filters
        
        async def async_handle(update: Update, context):
            handle_message(update, context)
            
        app.add_handler(NewMessageHandler(new_filters.TEXT & ~new_filters.COMMAND, async_handle))
        print("बॉट चालू हो गया है (वर्शन 20+)...")
        app.run_polling()

if __name__ == '__main__':
    main()
