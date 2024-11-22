import asyncio
from aiogram import Bot, Dispatcher
from config_reader import config
from database import db
from handlers import buttons_admin, buttons_user, command_handlers, none_filter
from utils.logger import setup_logger

# Настраиваем логгер
logger = setup_logger("bot.log", "INFO", True)

async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    
    dp.include_routers(command_handlers.router, buttons_admin.router, buttons_user.router, none_filter.router)
    
    logger.info("Bot has been started!")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    database = db.Database()
    database.create_init_db()
    asyncio.run(main())
