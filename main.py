import asyncio
import logging
import signal
from aiogram import Bot, Dispatcher
from config_data.config import load_config
from handlers import user_handlers, other_handlers
from keyboards.main_menu import set_main_menu
from logger.logger import setup_logger
from services.services import sigint_handler, sigterm_handler
from database.database import get_connection, create_tables


def init_db():
    try:
        db_connection = get_connection()
        create_tables(db_connection)
        logging.info('Database initialized successfully.')
    except Exception as e:
        logging.error(f"Error initializing database: {e}")


async def main():
    try:
        config = load_config()
        logging.info("Configuration loaded successfully.")
    except Exception as e:
        logging.error(f"Error loading configuration: {e}.")
        return

    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher()

    await set_main_menu(bot)

    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    setup_logger()

    init_db()

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(main())

    loop.add_signal_handler(signal.SIGTERM, sigterm_handler())
    loop.add_signal_handler(signal.SIGINT, sigint_handler())
