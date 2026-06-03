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
    """Sarvam AI को कॉल करने का फंक्शन"""
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
            return f"AI Error: {response.status_code}. कृपया कुछ समय बाद प्रयास करें।"
    except Exception as e:
        return f"Error: {str(e)}"

@bot.message_handler(func=lambda message: True)
def handle_incoming_messages(message):
    user_text = message.text
    chat_id = message.chat.id

    if not user_text:
        return

    # चेक करें कि क्या मैसेज में कोई लिंक (अमेज़न/फ्लिपकार्ट आदि) है
    urls = re.findall(r'(https?://[^\s]+)', user_text)

    if urls:
        # ---- सुपर अट्रैक्टिव डील मोड ----
        deal_instruction = (
            "You are a professional deals influencer on Telegram. Create a super catchy, high-converting, "
            "and attractive shopping deal post in Hinglish/Hindi mixed language. Use markdown formatting. "
            "Follow this structure precisely:\n"
            "🔥 LOOT DEAL /⚡ CRAZY OFFER (Bold Heading with emojis)\n"
            "📦 Product Name (bold)\n"
            "✨ Key Features/Highlights (Bullet points with nice emojis like ✅, ⭐)\n"
            "💰 Special Price Details\n"
            "👉 Grab it before it's gone!\n"
            "Make sure it looks extremely clean, modern, and exciting to read!"
        )
        
        bot.send_chat_action(chat_id, 'typing')
        ai_deal_post = call_sarvam_ai(user_text, deal_instruction)
        
        # सुंदर बटन्स (Inline Keyboards)
        markup = telebot.types.InlineKeyboardMarkup()
        btn_buy = telebot.types.InlineKeyboardButton(text="🛍️ BUY NOW (यहाँ से खरीदें)", url=urls[0])
        btn_join = telebot.types.InlineKeyboardButton(text="📢 Join Main Channel", url="https://t.me/your_channel") # अपना चैनल लिंक यहाँ बदलें
        btn_more = telebot.types.InlineKeyboardButton(text="✨ More Loot Deals", url="https://t.me/your_channel")
        
        markup.add(btn_buy)
        markup.add(btn_join, btn_more)
        
        # पोस्ट भेजना
        try:
            bot.send_message(chat_id, ai_deal_post, reply_markup=markup, parse_mode="Markdown")
        except Exception:
            # अगर मर्कडाउन में कोई दिक्कत आए, तो बिना मर्कडाउन के भेजें ताकि बोट क्रैश न हो
            bot.send_message(chat_id, ai_deal_post, reply_markup=markup)

    else:
        # ---- एक्टिव लाइव चैट / AI असिस्टेंट मोड ----
        chat_instruction = (
            "You are a friendly, cool, and smart AI Assistant talking live with a user on Telegram. "
            "Answer the user's queries in a natural, conversational, and helpful manner using a mix of Hindi and English (Hinglish). "
            "Keep your responses engaging, short, and to the point. Do not talk like a rigid machine. "
            "Be witty, helpful, and ready to guide them."
        )
        
        bot.send_chat_action(chat_id, 'typing')
        ai_chat_response = call_sarvam_ai(user_text, chat_instruction)
        
        # यूज़र के मैसेज का सीधे जवाब (लाइव चैट की तरह)
        bot.reply_to(message, ai_chat_response)

# बोट को स्टार्ट करना
if __name__ == "__main__":
    print("Bot is successfully running with Live Chat mode...")
    bot.infinity_polling()
    
