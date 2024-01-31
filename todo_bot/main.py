import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from config.config_reader import config
from handlers import handlers
from handlers import cmd

async def main():
    bot = Bot(token=config.API_TOKEN.get_secret_value(), parse_mode=ParseMode.HTML)
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_routers(handlers.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())