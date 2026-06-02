import os
import logging
import requests
import telebot

# --- RAILWAY ENVIRONMENT VARIABLES ---
# Code automatic aapke Railway Variables se keys utha lega
BOT_TOKEN = os.getenv("BOT_TOKEN")
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
CHANNEL_ID = "@dealsoffreedom"

# Affiliate Tags
AMAZON_TAG = "dealsoffreedom-21"
FLIPKART_ID = "dealsoffreedom"

# Logging setup for Railway
logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# Telebot initialization (Highly stable for cloud)
bot = telebot.TeleBot(BOT_TOKEN)

def get_sarvam_premium_caption(platform, url):
    """Sarvam AI Connection"""
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
        "2. Content ko bold karne ke liye Markdown format use karo.\n"
        "3. Slangs use karo jaise: 'Paisa Vasool Deal', 'Direct Loot', 'Bhaari Bachat', 'Miss mat karna bhaiyo'.\n"
        "4. Lines me gap rakho taaki padhne me maza aaye.\n"
        "5. Last line fix honi chahiye: 'Yahan se khareedein 👇'."
    )
    
    payload = {
        "model": "mayura-v1",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": f"Platform: {platform}\nLink: {url}\nIs product ke liye ek mast viral post likho."}
        ],
        "temperature": 0.85
    }
    
    try:
        response = requests.post(api_url, json=payload, headers=headers, timeout=10)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
    except Exception as e:
        logging.error(f"Sarvam Error: {e}")
    
    return f"🔥 **{platform} LOOT ALERT!** 🔥\n\n⚡ **Ekdum Mast Deal! Miss mat karo bhaiyo!**\n\nYahan se khareedein 👇"

def convert_to_affiliate(url):
    if "amazon" in url.lower():
        return f"{url}&tag={AMAZON_TAG}" if "?" in url else f"{url}?tag={AMAZON_TAG}"
    elif "flipkart" in url.lower():
        return f"{url}&affid={FLIPKART_ID}" if "?" in url else f"{url}?affid={FLIPKART_ID}"
    return url

# Message handler for shared links
@bot.message_handler(func=lambda message: message.text and "http" in message.text)
def handle_links(message):
    user_text = message.text
    status_msg = bot.reply_to(message, "⏳ Sarvam AI dhamakedar post bana raha hai...")
    
    platform = "Amazon" if "amazon" in user_text.lower() else "Flipkart" if "flipkart" in user_text.lower() else "Online Store"
    
    # Get content from Sarvam AI
    ai_caption = get_sarvam_premium_caption(platform, user_text)
    affiliate_link = convert_to_affiliate(user_text)
    
    final_post = f"{ai_caption}\n
    
