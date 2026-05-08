import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# گرفتن توکن‌ها از Environment Variables
BOT_TOKEN = os.getenv("8498029698:AAF0K4dzvx1ghL69mZyNLbKv7_9ntOLJxDY")
GEMINI_API_KEY = os.getenv("AIzaSyDyNN1jMucBrErcd-QRj8c4vNnONu26ac0")

# تنظیم Gemini
genai.configure(api_key=GEMINI_API_KEY)

# مدل جیمینای
model = genai.GenerativeModel("gemini-1.5-flash")


# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋\nربات جیمینای آماده است.")


# پاسخ به پیام‌ها
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = model.generate_content(user_message)

        await update.message.reply_text(response.text)

    except Exception as e:
        await update.message.reply_text(f"خطا:\n{e}")


def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("Bot is running...")

    app.run_polling()


if name == "main":
    main()
if name == "main":
    main()
