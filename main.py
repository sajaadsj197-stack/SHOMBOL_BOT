import google.generativeai as genai
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

# توکن ربات تلگرام
BOT_TOKEN = "8687879112:AAHvpvQpZrgNTYiWYpTpEHectPFtW7Lprco"

# کلید Gemini
GEMINI_API_KEY = "AIzaSyDyNN1jMucBrErcd-QRj8c4vNnONu26ac0"

# تنظیم Gemini
genai.configure(api_key=GEMINI_API_KEY)

# مدل جیمینای
model = genai.GenerativeModel("gemini-1.5-flash")


# دستور استارت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سلام 👋\nربات جیمینای فعال شد.")


# پاسخ به پیام‌ها
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    try:
        response = model.generate_content(user_message)

        await update.message.reply_text(response.text)

    except Exception as e:
        await update.message.reply_text(f"خطا:\n{e}")


# اجرای ربات
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    print("Bot is running...")

    app.run_polling()


# اجرای اصلی
if name == "main":
    main()
