import asyncio
from telegram import Bot
from config import TOKEN

URL = f"https://ai-tg-bot-lf1m.onrender.com/webhook/{TOKEN}"

async def main():
    bot = Bot(TOKEN)

    await bot.delete_webhook()
    await bot.set_webhook(url=URL)

    print("Webhook set:", URL)

asyncio.run(main())