async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):

    link = update.message.text.strip()

    if (
        "amazon" in link
        or "amzn.to" in link
        or "flipkart" in link
        or "myntra" in link
        or "ajio" in link
        or "meesho" in link
    ):

        keyboard = [
            [
                InlineKeyboardButton(
                    "🛒 Buy Now",
                    url=link
                )
            ],
            [
                InlineKeyboardButton(
                    "📢 Join Channel",
                    url="https://t.me/dealsoffreedom"
                ),
                InlineKeyboardButton(
                    "🔥 More Deals",
                    url="https://t.me/dealsoffreedom"
                )
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)

        caption = f"""
🔥 HOT DEAL ALERT 🔥

⚡ Best Price Online
💥 Limited Time Offer

👇 Buy From Button Below 👇

{link}
"""

        # PHOTO + BUTTON TOGETHER
        await context.bot.send_message(
            chat_id=CHANNEL_ID,
            text=caption,
            reply_markup=reply_markup,
            disable_web_page_preview=False
        )

        await update.message.reply_text(
            "✅ Deal Posted Successfully 🚀"
        )

    else:

        await update.message.reply_text(
            "❌ Send Valid Shopping Product Link"
        )
