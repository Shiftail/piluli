import asyncio
from aiogram import Bot, Dispatcher
from config import load_config
from handlers import register_handlers

async def main():
    config = load_config()
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    register_handlers(dp)
    print("Бот запущен!")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
