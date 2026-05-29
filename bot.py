import re
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# आपके एफिलिएट टैग्स / ट्रैकिंग आईडी
AMAZON_TAG = "your_amazon_tag-21"
FLIPKART_AFF_ID = "your_flipkart_id"

# आपके चैनल और अन्य लिंक्स (इन्हें बदल लें)
CHANNEL_USERNAME = "@dealsoffreedom"  # आपके चैनल का यूजरनेम
CHANNEL_LINK = "https://t.me/dealsoffreedom"  # चैनल का इनवाइट लिंक
MORE_DEALS_LINK = "https://t.me/dealsoffreedom"  # या आपकी कोई वेबसाइट/दूसरा लिंक

def modify_link(original_url):
    """विभिन्न शॉपिंग वेबसाइट्स के लिंक्स को एफिलिएट लिंक में बदलना"""
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

    # मैसेज में से पहला URL ढूंढना (Buy Now बटन के लिए)
    urls = re.findall(r'(https?://[^\s]+)', text)
    
    if urls:
        buy_now_url = modify_link(urls[0])  # पहली लिंक को एफिलिएट लिंक में बदलें
        
        # बाकी लिंक्स को भी मैसेज टेक्स्ट में रिप्लेस करना
        modified_text = text
        for url in urls:
            new_url = modify_link(url)
            modified_text = modified_text.replace(url, new_url)
        
        # 🌟 नया फीचर: मैसेज के ऊपर एक आकर्षक 'New Deal' हेडिंग जोड़ना
        final_message_text = f"🔥 **NEW BLAST DEAL** 🔥\n\n{modified_text}"
        
        # 🔘 इनलाइन बटन्स (Inline Keyboard) तैयार करना
        keyboard = [
            [InlineKeyboardButton("🛒 Buy Now (खरीदें)", url=buy_now_url)],
            [
                InlineKeyboardButton("📢 Join Channel", url=CHANNEL_LINK),
                InlineKeyboardButton("🛍️ More Deals", url=MORE_DEALS_LINK)
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        # टेलीग्राम चैनल पर बटन के साथ पोस्ट भेजना
        await context.bot.send_message(
            chat_id=CHANNEL_USERNAME, 
            text=final_message_text, 
            reply_markup=reply_markup,
            parse_mode="Markdown"  # ताकि बोल्ड टेक्स्ट (** बोल्ड **) सही से दिखे
        )
        
        # बोट चैट में आपको कन्फर्मेशन मिलना
        await update.message.reply_text("✅ डील बटन्स और न्यू अपडेट हेडिंग के साथ चैनल पर पोस्ट हो गई है!")

if __name__ == '__main__':
    BOT_TOKEN = "8601951285:AAE09-x_4Peuh3WSJN68U21iGFKsCuVnLLE"
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("बॉट चालू है और बटन्स के साथ डील्स पोस्ट करने के लिए तैयार है...")
    app.run_polling()
