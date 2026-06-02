import logging
import requests
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# --- CONFIGURATION ---
BOT_TOKEN = "8601951285:AAE09-x_4Peuh3WSJN68U21iGFKsCuVnLLE"
SARVAM_API_KEY = "sk_6ahjv2o0_IIpdnV9xKVV7JpuebfkgbREJ"
CHANNEL_ID = "@dealsoffreedom"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def fetch_product_info(url):
    """Link se Product Name aur Price nikalna"""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(r.content, 'html.parser')
        
        # Amazon/Flipkart specific selectors
        title = soup.title.string[:50] if soup.title else "New Deal!"
        return title
    except:
        return "New Awesome Product"

def get_sarvam_caption(title, url):
    """Sarvam AI se catchy Hinglish caption generate karna"""
    api_url = "https://api.sarvam.ai/v1/chat/completions"
    headers = {"api-key": SARVAM_API_KEY, "Content-Type": "application/json"}
    
    prompt = f"Product: {title}. Iske liye ek viral, short, Hinglish Telegram deal post likho @dealsoffreedom ke liye. Emojis use karo, excitement badhao, aur price point highlight karo. Last mein likho: 'Yahan se khareedein 👇'"
    
    payload = {
        "model": "mayura-v1",
        "messages": [{"role": "user", "content": prompt}]
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        return response.json()['choices'][0]['message']['content']
    except:
        return f"🔥 Loot Deal Alert!\n{title}\n\nCheck out here: {url}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Link aate hi process karna"""
    user_text = update.message.text
    
    # Check agar link hai
    if "http" in user_text:
        await update.message.reply_text("⏳ Processing deal with Sarvam AI...")
        
        # 1. Fetch info
        title = fetch_product_info(user_text)
        
        # 2. Get AI Caption
        caption = get_sarvam_caption(title, user_text)
        
        # 3. Post to Channel
        final_message = f"{caption}\n\n🔗 {user_text}"
        await context.bot.send_message(chat_id=CHANNEL_ID, text=final_message)
        
        await update.message.reply_text("✅ Deal successfully posted to @dealsoffreedom!")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot is running...")
    app.run_polling()
    
