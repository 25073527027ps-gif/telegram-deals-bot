import logging
import re
import requests
import cloudscraper
from bs4 import BeautifulSoup
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# --- CONFIGURATION ---
BOT_TOKEN = "8601951285:AAE09-x_4Peuh3WSJN68U21iGFKsCuVnLLE"
SARVAM_API_KEY = "sk_6ahjv2o0_IIpdnV9xKVV7JpuebfkgbRE"
CHANNEL_ID = "@dealsoffreedom"

# Affiliate Tags (Apne actual tags se badlein)
AMAZON_TAG = "dealsoffreedom-21"
FLIPKART_ID = "dealsoffreedom"

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def clean_price(price_str):
    """Price string se numbers nikalna (e.g., '₹1,499' -> 1499)"""
    nums = re.findall(r'\d+', price_str.replace(',', ''))
    return int(nums[0]) if nums else 0

def fetch_product_details(url):
    """Amazon aur Flipkart se automatic Name, Price aur MRP nikalna"""
    scraper = cloudscraper.create_scraper()
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        response = scraper.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        title, current_price, mrp = "Product", "Check Link", "0"
        
        # --- AMAZON SCRAPER ---
        if "amazon" in url.lower():
            title_tag = soup.find("span", id="productTitle")
            title = title_tag.get_text().strip() if title_tag else "Amazon Product"
            
            price_tag = soup.find("span", class_="a-price-whole")
            current_price = f"₹{price_tag.get_text().strip()}" if price_tag else "Special Price"
            
            mrp_tag = soup.find("span", class_="a-price a-text-price")
            if mrp_tag:
                mrp_span = mrp_tag.find("span", class_="a-offscreen")
                mrp = mrp_span.get_text().strip() if mrp_span else "0"
                
        # --- FLIPKART SCRAPER ---
        elif "flipkart" in url.lower():
            title_tag = soup.find("span", class_="B_NuCI")
            title = title_tag.get_text().strip() if title_tag else "Flipkart Product"
            
            price_tag = soup.find("div", class_="_30jeq3 _16Jk6d")
            current_price = price_tag.get_text().strip() if price_tag else "Special Price"
            
            mrp_tag = soup.find("div", class_="_3I9_wX _273_aA")
            mrp = mrp_tag.get_text().strip() if mrp_tag else "0"

        # --- DISCOUNT CALCULATOR ---
        discount_percent = 0
        c_val = clean_price(current_price)
        m_val = clean_price(mrp)
        if m_val > c_val and c_val > 0:
            discount_percent = round(((m_val - c_val) / m_val) * 100)

        # Title ko clean aur thoda chota karna
        clean_title = ' '.join(title.split()[:8])
        return clean_title, current_price, mrp, discount_percent

except Exception as e:
        print(f"Scraping Error: {e}")
        return "Special Deal", "Best Price", "0", 0

def get_sarvam_premium_caption(platform, title, price, mrp, discount):
    """Sarvam AI se professional, high-hype, category-based caption nikalna"""
    api_url = "https://api.sarvam.ai/v1/chat/completions"
    headers = {"api-key": SARVAM_API_KEY, "Content-Type": "application/json"}
    
    # Auto Category detection
    category = "#Loot"
    lower_title = title.lower()
    if any(x in lower_title for x in ["phone", "mobile", "laptop", "earbuds", "tws", "watch", "charger"]):
        category = "#Electronics"
    elif any(x in lower_title for x in ["shoes", "t-shirt", "jeans", "shirt", "jacket", "kurta"]):
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
        response = requests.post(api_url, json=payload, headers=headers)
        return response.json()['choices'][0]['message']['content'], category
    except:
        # Fallback Caption agar AI down ho
        fallback = f"🔥 **{platform} LOOT ALERT!** 🔥\n\n📦 **{title}**\n💰 Price: {price} (~~{mrp}~~) \n⚡ **{discount}% Ki Bhaari Bachat!**\n\nYahan se khareedein 👇"
        return fallback, category

def convert_to_affiliate(url):
    """Automatic normal link ko affiliate link me convert karna"""
    if "amazon" in url.lower():
        if "?" in url:
            return f"{url}&tag={AMAZON_TAG}"
        return f"{url}?tag={AMAZON_TAG}"
    elif "flipkart" in url.lower():
        if "?" in url:
            return f"{url}&affid={FLIPKART_ID}"
        return f"{url}?affid={FLIPKART_ID}"
    return url

async def handle_incoming_deal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    
    if "http" in user_text:
        status_msg = await update.message.reply_text("🕵️‍♂️ Fetching live prices & creating AI content...")
        
        # 1. Platform Detect Karein
        platform = "Amazon" if "amazon" in user_text.lower() else "Flipkart" if "flipkart" in user_text.lower() else "Online Store"
        
        # 2. Scrape Details
        title, price, mrp, discount = fetch_product_details(user_text)
        
        # 3. Get Premium Sarvam AI Caption
        ai_caption, category = get_sarvam_premium_caption(platform, title, price, mrp, discount)
        
        # 4. Generate Affiliate Link
        affiliate_link = convert_to_affiliate(user_text)
        
        # 5. Final Post Compilation
        final_post = f"{ai_caption}\n🔗 {affiliate_link}\n\n📢 Join: {CHANNEL_ID} {category}"
        
        # 6. Post to Channel with Markdown formatting
        try:
            await context.bot.send_message(chat_id=CHANNEL_ID, text=final_post, parse_mode="Markdown")
            await status_msg.edit_text("🚀 Boom! Deal is automatically live on @dealsoffreedom!")
        except Exception as telegram_error:
            # Agar Markdown format me koi symbol error de, to plain text bhejega
            await context.bot.send_message(chat_id=CHANNEL_ID, text=final_post)
            await status_msg.edit_text("✅ Live on channel (Plain Format)!")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_incoming_deal))
    print("🤖 Your AI Premium Affiliate Bot is Active and Listening...")
    app.run_polling()
                                        
