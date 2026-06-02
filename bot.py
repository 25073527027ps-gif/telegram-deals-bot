import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# --- RAILWAY ENVIRONMENT VARIABLES ---
BOT_TOKEN = os.getenv("8601951285:AAE09-x_4Peuh3WSJN68U21iGFKsCuVnLLE")
SARVAM_API_KEY = os.getenv("sk_7lrqry6r_hirqUMieRE3WoAmHhDS0f9Cw")
CHANNEL_ID = "@dealsoffreedom"

# Affiliate Tags
AMAZON_TAG = "dealsoffreedom-21"
FLIPKART_ID = "dealsoffreedom"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def get_sarvam_premium_caption(platform, url):
    """Sarvam AI Connection - Simple & Safe for Cloud Deployments"""
    api_url = "https://api.sarvam.ai/v1/chat/completions"
    headers = {
        "api-key": SARVAM_API_KEY, 
        "Content-Type": "application/json"
    }
    
    system_instruction = (
        "Tum Telegram channel '@dealsoffreedom' ke master admin aur sales expert ho. "
        "Tumhara kaam ek dum dhasu, high-energy Hinglish post banana hai jo click karne par majboor kare. "
        "Strict Formatting Rules:\n"
        "1. Emojis ka bhayankar aur badhiya use karo (🔥, ⚡, 🚨, 💸, 🏃‍♂️💨).\n"
        "2. Product ka Naam aur loot price apne dimaag se bold (**text**) me acche se highlight karo.\n"
        "3. Slangs use karo jaise: 'Paisa Vasool Deal', 'Direct Loot', 'Bhaari Bachat', 'Miss mat karna bhaiyo'.\n"
        "4. Lines me gap rakho taaki padhne me maza aaye.\n"
        "5. Last line fix honi chahiye: 'Yahan se khareedein 👇'."
    )
    
    user_data = f"Platform: {platform}\nProduct Link: {url}\n\nIs link ke liye ek ekdam khatarnak deal post taiyar karo."
    
    payload = {
        "model": "mayura-v1",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_data}
        ],
        "temperature": 0.85
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Sarvam API error: {e}")
    
    return f"🔥 **{platform} LOOT ALERT!** 🔥\n\n⚡ **Ekdum Mast Deal! Miss mat karo bhaiyo!**\n\nYahan se khareedein 👇"

def convert_to_affiliate(url):
    """Normal link ko affiliate me convert karna"""
    if "amazon" in url.lower():
        return f"{url}&tag={AMAZON_TAG}" if "?" in url else f"{url}?tag={AMAZON_TAG}"
    elif "flipkart" in url.lower():
        return f"{url}&affid={FLIPKART_ID}" if "?" in url else f"{url}?affid={FLIPKART_ID}"
    return url

async def handle_incoming_deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if not user_text or "http" not in user_text:
        return

    status_msg = await update.message.reply_text("⏳ Sarvam AI post bana raha hai...")
    
    platform = "Amazon" if "amazon" in user_text.lower() else "Flipkart" if "flipkart" in user_text.lower() else "Online Store"
    
    # Generate content via Sarvam AI
    ai_caption = get_sarvam_premium_caption(platform, user_text)
    affiliate_link = convert_to_affiliate(user_text)
    
    final_post = f"{ai_caption}\n🔗 {affiliate_link}\n\n📢 Join: {CHANNEL_ID}"
    
    try:
        await context.bot.send_message(chat_id=CHANNEL_ID, text=final_post, parse_mode="Markdown")
        await status_msg.edit_text("🚀 Boom! Deal is live on @dealsoffreedom!")
    except Exception as e:
        await context.bot.send_message(chat_id=CHANNEL_ID, text=final_post)
        await status_msg.edit_text("✅ Deal posted successfully (Safe Text)!")

if __name__ == '__main__':
    if not BOT_TOKEN or not SARVAM_API_KEY:
        print("CRITICAL ERROR: BOT_TOKEN or SARVAM_API_KEY missing!")
        exit(1)
        
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_incoming_deal))
    print("🤖 Bot is completely live on Railway...")
    app.run_polling()
    
