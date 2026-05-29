import re
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# आपके एफिलिएट टैग्स / ट्रैकिंग आईडी
AMAZON_TAG = "your_amazon_tag-21"
FLIPKART_AFF_ID = "your_flipkart_id"

def modify_link(original_url):
    """
    विभिन्न शॉपिंग वेबसाइट्स के लिंक्स को पहचान कर उन्हें एफिलिएट लिंक में बदलना
    """
    # 1. AMAZON LINK CHECK
    if "amazon.in" in original_url or "amzn.to" in original_url:
        # अगर लिंक में पहले से कोई टैग है तो उसे हटाकर अपना टैग जोड़ना
        clean_url = re.sub(r'tag=[^&]+', '', original_url)
        connector = "&" if "?" in clean_url else "?"
        return f"{clean_url.strip()}{connector}tag={AMAZON_TAG}"

    # 2. FLIPKART LINK CHECK
    elif "flipkart.com" in original_url:
        connector = "&" if "?" in original_url else "?"
        return f"{original_url.strip()}{connector}affid={FLIPKART_AFF_ID}"

    # 3. MYNTRA LINK CHECK
    elif "myntra.com" in original_url:
        # आप अपनी मायन्त्रा एफिलिएट नेटवर्क (जैसे EarnKaro/Cuelinks) का सब-आईडी यहाँ जोड़ सकते हैं
        return original_url.strip()

    # 4. AJIO LINK CHECK
    elif "ajio.com" in original_url:
        return original_url.strip()

    # अगर कोई अन्य लिंक है तो उसे बिना बदलाव के भेजें
    return original_url

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    if not text:
        return

    # मैसेज में से यूआरएल (URLs) ढूंढना
    urls = re.findall(r'(https?://[^\s]+)', text)
    
    if urls:
        modified_text = text
        for url in urls:
            new_url = modify_link(url)
            modified_text = modified_text.replace(url, new_url)
        
        # आपके डील्स चैनल की आईडी (यहाँ अपनी चैनल आईडी डालें जैसे '@dealsoffreedom')
        TARGET_CHANNEL = "@dealsoffreedom" 
        
        # चैनल पर ऑटोमेटिक पोस्ट भेजना
        await context.bot.send_message(chat_id=TARGET_CHANNEL, text=modified_text)
        
        # आपको बोट चैट में कन्फर्मेशन मिलना
        await update.message.reply_text("✅ डील सफलताबाूर्वक चैनल पर अपलोड हो गई है!")

if __name__ == '__main__':
    # अपना टेलीग्राम बोट टोकन यहाँ डालें
    BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
    
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # हर टेक्स्ट मैसेज को चेक करने के लिए हैंडलर
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("बॉट चालू हो गया है और लिंक्स की निगरानी कर रहा है...")
    app.run_polling()
