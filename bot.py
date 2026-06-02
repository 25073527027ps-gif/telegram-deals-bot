from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
import requests

BOT_TOKEN = "8601951285:AAE09-x_4Peuh3WSJN68U21iGFKsCuVnLLE"
SARVAM_API_KEY = "sk_6ahjv2o0_IIpdnV9xKVV7JpuebfkgbREJ"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Product details bhejo, main Hindi reel script banaunga."
    )

async def generate_script(update: Update, context: ContextTypes.DEFAULT_TYPE):

    product = update.message.text

    prompt = f"""
    Is product ke liye 40 second ki Hindi Instagram Reel script likho:
    {product}

    End me CTA add karo:
    'Agar link chahiye to comment me LINK likhen'
    """

    headers = {
        "Authorization": f"Bearer {SARVAM_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        "https://api.sarvam.ai/v1/chat/completions",
        headers=headers,
        json=payload
    )

    result = response.json()

    script = result["choices"][0]["message"]["content"]

    await update.message.reply_text(script)

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, generate_script))

app.run_polling()
