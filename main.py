import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from dotenv import load_dotenv

from handlers import commands
from database.db import init_db

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

async def main():
    logging.basicConfig(level=logging.INFO)

    await init_db()

    bot = Bot(
        token=TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()

    dp.include_router(commands.router)

    print("Бот запущен")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())