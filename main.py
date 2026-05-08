import os
import logging
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, MessageHandler, ContextTypes, filters
from google import genai

logging.basicConfig(level=logging.INFO)

TELEGRAM_BOT_TOKEN = os.environ["8498029698:AAF0K4dzvx1ghL69mZyNLbKv7_9ntOLJxDY"]
GEMINI_API_KEY = os.environ["AIzaSyDyNN1jMucBrErcd-QRj8c4vNnONu26ac0"]
WEBHOOK_URL = os.environ["WEBHOOK_URL"]

app = Flask(__name__)
client = genai.Client(api_key=GEMINI_API_KEY)
tg_app = Application.builder().token(TELEGRAM_BOT_TOKEN).updater(None).build()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=user_text
        )
        answer = response.text if response.text else "No response."
    except Exception as e:
        answer = f"Error: {e}"
    await update.message.reply_text(answer)

tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route("/webhook", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, tg_app.bot)
    await tg_app.process_update(update)
    return "ok"

@app.route("/")
def home():
    return "Bot is running"

if __name__ == "__main__":
    import asyncio

    async def main():
        async with tg_app:
            await tg_app.start()
            await tg_app.bot.set_webhook(url=f"{WEBHOOK_URL}/webhook")
            await asyncio.Event().wait()

    asyncio.run(main())
