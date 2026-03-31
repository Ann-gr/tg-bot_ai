import threading
from flask import Flask

from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters

from config import TOKEN
from handlers.commands import start, help_command
from handlers.messages import handle_message

app_flask = Flask(__name__)


@app_flask.route("/")
def home():
    return "Bot is running!"


def run_bot():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    # запускаем бота в отдельном потоке
    threading.Thread(target=run_bot).start()

    # запускаем веб-сервер (Render доволен)
    app_flask.run(host="0.0.0.0", port=10000)