import asyncio
from aiogram import Bot, Dispatcher
from config_reader import config
from database import db
from handlers import buttons_admin, buttons_user, command_handlers, none_filter, compliments_female
from utils.logger import setup_logger

logger = setup_logger("bot.log", "INFO", True)
database = db.Database()

async def restore_user_states(dp: Dispatcher, database):
    users = database.get_all_users()
    for user in users:
        user_id = user[1]  
        user_state = user[7]
        print("User id: ", user_id)
        print("User state: ", user_state)
        await dp.storage.update_data(user_id, {'state': user_state})
        logger.info(f"Restored user {user_id} state: {user_state}")


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    
    dp.include_routers(command_handlers.router, 
                       buttons_admin.router, 
                       buttons_user.router, 
                       compliments_female.router,
                       none_filter.router)
    
    logger.info("Bot has been started!")
    
    await restore_user_states(dp, database)
    
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
    
if __name__ == "__main__":
    database.create_init_db()
    asyncio.run(main())
