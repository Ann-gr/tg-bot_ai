from flask import Flask, request
from telegram import Update, Bot
from config import TOKEN
import os
import asyncio

app = Flask(__name__)
bot = Bot(TOKEN)

@app.route("/", methods=["GET"])
def home():
    return "Bot is running"

@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    try:
        print("🔥 WEBHOOK HIT")

        data = request.get_json(force=True)
        update = Update.de_json(data, bot)

        if update.message and update.message.text:
            text = update.message.text

            if text == "/start":
                asyncio.run(
                    bot.send_message(
                        chat_id=update.message.chat.id,
                        text="Бот работает 🚀"
                    )
                )
            else:
                asyncio.run(
                    bot.send_message(
                        chat_id=update.message.chat.id,
                        text=f"Ты написал: {text}"
                    )
                )

        return "ok", 200

    except Exception as e:
        print("❌ ERROR:", e)
        return "error", 200

if __name__ == "__main__":
    print("Starting bot...")

    PORT = int(os.getenv("PORT", 10000))
    app.run(host="0.0.0.0", port=PORT)