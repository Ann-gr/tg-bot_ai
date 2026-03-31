from flask import Flask, request
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import os
from config import TOKEN

app = Flask(__name__)

# создаём telegram app
tg_app = ApplicationBuilder().token(TOKEN).build()


# handlers
async def start(update, context):
    await update.message.reply_text("Бот работает 🚀")


async def echo(update, context):
    await update.message.reply_text(update.message.text)


tg_app.add_handler(CommandHandler("start", start))
tg_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


# webhook endpoint
@app.route(f"/webhook/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), tg_app.bot)

    tg_app.create_task(tg_app.process_update(update))

    return "ok"


# health check (Render требует)
@app.route("/", methods=["GET"])
def home():
    return "Bot is running"


# запуск webhook
def set_webhook():
    url = f"https://ai-tg-bot-lf1m.onrender.com/webhook/{TOKEN}"
    tg_app.bot.set_webhook(url=url)


if __name__ == "__main__":
    set_webhook()
    app.run(host="0.0.0.0", port=10000)