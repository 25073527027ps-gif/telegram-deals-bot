import os
import re
import requests
import telebot

# Telegram Bot Token (Railway की Environment Variables से लेगा)
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

# Sarvam AI API Configuration
SARVAM_API_KEY = os.getenv("SARVAM_API_KEY")
SARVAM_URL = "https://api.sarvam.ai/v1/chat/completions"

def call_sarvam_ai(prompt, system_instruction):
    """Sarvam AI को कॉल करने और रिस्पॉन्स पाने का फंक्शन"""
    if not SARVAM_API_KEY:
        return "Error: Sarvam AI API Key missing!"
        
    headers = {
        "Content-Type": "application/json",
        "api-subscription-key": SARVAM_API_KEY
    }
    
    payload = {
        "model": "sarvam-2b",
        "messages": [
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ]
    }
    
    try:
        response = requests.post(SARVAM_URL, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"AI Error: {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@bot.message_handler(func=lambda message: True)
def handle_incoming_messages(message):
    user_text = message.text
    chat_id = message.chat.id

    # चेक करें कि क्या मैसेज में कोई लिंक (अमेज़न/फ्लिपकार्ट आदि) है
    urls = re.findall(r'(https?://[^\s]+)', user_text)

    if urls:
        # ---- DEAL GENERATION MODE ----
        # अगर लिंक है, तो इसे डील पोस्ट में बदलने के लिए Sarvam AI को निर्देश दें
        deal_instruction = (
            "You are an expert affiliate marketer. Create an attractive, catchy telegram post for this product link. "
            "Use appropriate emojis, highlight key features, and make it look professional in Hindi/English mixed language."
        )
        
        bot.send_chat_action(chat_id, 'typing')
        ai_deal_post = call_sarvam_ai(user_text, deal_instruction)
        
        # बटन (Inline Keyboards) तैयार करना
        markup = telebot.types.InlineKeyboardMarkup()
        btn_buy = telebot.types.InlineKeyboardButton(text="🛍️ Buy Now", url=urls[0])
        btn_join = telebot.types.InlineKeyboardButton(text="📢 Join Channel", url="https://t.edges.com/your_channel") # अपना चैनल लिंक डालें
        btn_more = telebot.types.InlineKeyboardButton(text="✨ More Deals", url="https://t.edges.com/your_channel")
        
        markup.add(btn_buy)
        markup.add(btn_join, btn_more)
        
        # चैनल या यूजर को पोस्ट भेजना
        bot.send_message(chat_id, ai_deal_post, reply_markup=markup, parse_mode="Markdown")

    else:
        # ---- LIVE CHAT / AI ASSISTANT MODE ----
        # अगर कोई लिंक नहीं है, तो सामान्य बातचीत या सवाल का जवाब देने के लिए लाइव चैट मोड
        chat_instruction = (
            "You are a helpful, friendly, and smart AI assistant. Answer the user's queries accurately, "
            "keep the tone polite, and assist them with whatever they ask in a conversational manner in Hindi or Hinglish."
        )
        
        bot.send_chat_action(chat_id, 'typing')
        ai_chat_response = call_sarvam_ai(user_text, chat_instruction)
        
        # सामान्य चैट में बिना बटन के सीधे जवाब भेजना
        bot.reply_to(message, ai_chat_response)

# बोट को स्टार्ट करना
if __name__ == "__main__":
    print("Bot is running...")
    bot.infinity_polling()
    
