import asyncio
import logging

from aiogram import Bot, Dispatcher

from config_reader import config
from database import db
from handlers import cmd

logging.basicConfig(level=logging.INFO)
    
async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    
    dp.include_router(cmd.router)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    database = db.Database()
    database.create_init_db()
    asyncio.run(main())