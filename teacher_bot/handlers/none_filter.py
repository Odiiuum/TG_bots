from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message

router = Router()

# @router.message(StateFilter(None))
# async def handle_message_without_state(message: Message):
#     await message.answer("Для роботи бота введіть команду /start")
    
@router.message()
async def handle_message_without_state_none_filter(message: Message):
    await message.reply("Бот не має такої команди, спробуйте знову")
    