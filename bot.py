import os
import logging
import requests
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# --- CONFIGURATION FROM ENVIRONMENT VARIABLES ---
BOT_TOKEN = os.getenv("8601951285:AAE09-x_4Peuh3WSJN68U21iGFKsCuVnLLE")
SARVAM_API_KEY = os.getenv("sk_6ahjv2o0_IIpdnV9xKVV7JpuebfkgbRE")
CHANNEL_ID = "@dealsoffreedom"
AMAZON_TAG = "dealsoffreedom-21"
FLIPKART_ID = "dealsoffreedom"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- DUMMY WEB SERVER TO TRICK RAILWAY FROM CRASHING ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Bot is alive and running successfully!")

def run_dummy_server():
    port = int(os.getenv("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    logging.info(f"Dummy web server started on port {port}")
    server.serve_forever()

# --- ORIGINAL BOT LOGIC ---
def get_sarvam_premium_caption(platform, url):
    api_url = "https://api.sarvam.ai/v1/chat/completions"
    headers = {"api-key": SARVAM_API_KEY, "Content-Type": "application/json"}
    
    system_instruction = (
        "Tum Telegram channel '@dealsoffreedom' ke master admin aur sales expert ho. "
        "Tumhara kaam product details lekar ek dum dhasu, high-energy Hinglish post banana hai jo click karne par majboor kare. "
        "Strict Formatting Rules:\n"
        "1. Emojis ka bhayankar aur badhiya use karo (🔥, ⚡, 🚨, 💸, 🏃‍♂️💨).\n"
        "2. Product ka Naam aur loot price apne dimaag se bold (**text**) me acche se highlight karo.\n"
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

async def handle_incoming_deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    if not user_text or "http" not in user_text:
        return

    status_msg = await update.message.reply_text("⏳ Sarvam AI post bana raha hai...")
    platform = "Amazon" if "amazon" in user_text.lower() else "Flipkart" if "flipkart" in user_text.lower() else "Online Store"
    
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
        print("CRITICAL ERROR: Tokens missing in Environment Variables!")
        exit(1)
    
    # Background me dummy server chalana taaki Railway bot ko crash na kare
    threading.Thread(target=run_dummy_server, daemon=True).start()
    
    # Telegram Bot Polling Start karna
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_incoming_deal))
    print("🤖 Crash-proof Bot is fully active...")
    app.run_polling()
    
