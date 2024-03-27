import asyncio
import logging
from aiogram import Bot, Dispatcher
from config_data.config import load_config
from handlers import user_handlers, other_handlers
from keyboards.main_menu import set_main_menu
from logger.logger import setup_logger


async def main():
    setup_logger()

    try:
        config = load_config()
        logging.info("Configuration loaded successfully")
    except Exception as e:
        logging.error(f"Error loading configuration: {e}")
        return

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    await set_main_menu(bot)

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
