import os
import logging
import re
import requests
import cloudscraper
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# --- RAILWAY ENVIRONMENT VARIABLES ---
# Token aur Keys ko direct code me nahi, Railway dashboard par set karna hai
BOT_TOKEN = os.getenv("8601951285:AAE09-x_4Peuh3WSJN68U21iGFKsCuVnLLE")
SARVAM_API_KEY = os.getenv("sk_7lrqry6r_hirqUMieRE3WoAmHhDS0f9Cw")
CHANNEL_ID = "@dealsoffreedom"

# Affiliate Tags
AMAZON_TAG = "dealsoffreedom-21"
FLIPKART_ID = "dealsoffreedom"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def clean_price(price_str):
    try:
        nums = re.findall(r'\d+', price_str.replace(',', ''))
        return int(nums[0]) if nums else 0
    except:
        return 0

def fetch_product_details(url):
    """Scraper jo crash nahi hoga aur dynamic data nikalega"""
    try:
        scraper = cloudscraper.create_scraper()
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
        
        response = scraper.get(url, headers=headers, timeout=15)
        # Railway par html5lib ya lxml ke crash se bachne ke liye standard html.parser
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title, current_price, mrp = "Premium Product", "Check Live Price", "0"
        
        # --- AMAZON ---
        if "amazon" in url.lower():
            title_tag = soup.find("span", id="productTitle")
            if title_tag: title = title_tag.get_text().strip()
            
            price_tag = soup.find("span", class_="a-price-whole")
            if price_tag: current_price = f"₹{price_tag.get_text().strip()}"
            
            mrp_tag = soup.find("span", class_="a-price a-text-price")
            if mrp_tag:
                mrp_span = mrp_tag.find("span", class_="a-offscreen")
                if mrp_span: mrp = mrp_span.get_text().strip()
                
        # --- FLIPKART ---
        elif "flipkart" in url.lower():
            title_tag = soup.find("span", class_="B_NuCI") or soup.find("h1")
            if title_tag: title = title_tag.get_text().strip()
            
            price_tag = soup.find("div", class_="_30jeq3 _16Jk6d")
            if price_tag: current_price = price_tag.get_text().strip()
            
            mrp_tag = soup.find("div", class_="_3I9_wX _273_aA")
            if mrp_tag: mrp = mrp_tag.get_text().strip()

        # Discount Count
        discount_percent = 0
        c_val = clean_price(current_price)
        m_val = clean_price(mrp)
        if m_val > c_val and c_val > 0:
            discount_percent = round(((m_val - c_val) / m_val) * 100)

        clean_title = ' '.join(title.split()[:8])
        return clean_title, current_price, mrp, discount_percent

    except Exception as e:
        logging.error(f"Scraping failed safely: {e}")
        return "Special Deal", "Best Offer", "0", 0

def get_sarvam_premium_caption(platform, title, price, mrp, discount):
    """Sarvam AI Connection"""
    api_url = "https://api.sarvam.ai/v1/chat/completions"
    headers = {"api-key": SARVAM_API_KEY, "Content-Type": "application/json"}
    
    category = "#Loot"
    lower_title = title.lower()
    if any(x in lower_title for x in ["phone", "mobile", "laptop", "earbuds", "tws", "watch", "charger", "tv"]):
        category = "#Electronics"
    elif any(x in lower_title for x in ["shoes", "t-shirt", "jeans", "shirt", "jacket", "kurta", "saree"]):
        category = "#Fashion"

    system_instruction = (
        "Tum Telegram channel '@dealsoffreedom' ke master admin aur sales expert ho. "
        "Tumhara kaam product details lekar ek dum dhasu, high-energy Hinglish post banana hai jo click karne par majboor kare. "
        "Strict Formatting Rules:\n"
        "1. Emojis ka bhayankar aur badhiya use karo (🔥, ⚡, 🚨, 💸, 🏃‍♂️💨).\n"
        "2. Product ka Naam, Price, aur Discount hamesha BOLD (**text**) rakho.\n"
        "3. Slangs use karo jaise: 'Paisa Vasool Deal', 'Direct Loot', 'Bhaari Bachat', 'Miss mat karna bhaiyo'.\n"
        "4. Lines me gap rakho taaki padhne me maza aaye.\n"
        "5. Last line fix honi chahiye: 'Yahan se khareedein 👇'."
    )
    
    user_data = f"Platform: {platform}\nProduct: {title}\nLoot Price: {price}\nMRP: {mrp}\nDiscount: {discount}% OFF"
    
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
            return response.json()['choices'][0]['message']['content'], category
    except Exception as e:
        logging.error(f"Sarvam API failed safely: {e}")
    
    fallback = f"🔥 **{platform} LOOT ALERT!** 🔥\n\n📦 **{title}**\n💰 Price: {price} \n⚡ **Ekdum Mast Deal! Miss mat karo bhaiyo!**\n\nYahan se khareedein 👇"
    return fallback, category

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

    status_msg = await update.message.reply_text("🕵️‍♂️ Live price track ho raha hai aur Sarvam AI post bana raha hai...")
    
    platform = "Amazon" if "amazon" in user_text.lower() else "Flipkart" if "flipkart" in user_text.lower() else "Online Store"
    title, price, mrp, discount = fetch_product_details(user_text)
    ai_caption, category = get_sarvam_premium_caption(platform, title, price, mrp, discount)
    affiliate_link = convert_to_affiliate(user_text)
    
    final_post = f"{ai_caption}\n🔗 {affiliate_link}\n\n📢 Join: {CHANNEL_ID} {category}"
    
    try:
        await context.bot.send_message(chat_id=CHANNEL_ID, text=final_post, parse_mode="Markdown")
        await status_msg.edit_text("🚀 Boom! Deal is automatically live on @dealsoffreedom!")
    except Exception as e:
        # Fallback agar Markdown sync text crash kare
        await context.bot.send_message(chat_id=CHANNEL_ID, text=final_post)
        await status_msg.edit_text("✅ Deal posted successfully (Safe Text format)!")

if __name__ == '__main__':
    # Fail-safe check for Railway tokens
    if not BOT_TOKEN or not SARVAM_API_KEY:
        print("CRITICAL ERROR: BOT_TOKEN or SARVAM_API_KEY environment variables are missing!")
        exit(1)
        
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_incoming_deal))
    print("🤖 Crash-Proof Bot is fully online...")
    app.run_polling()
    
