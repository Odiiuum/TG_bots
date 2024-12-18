from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from database import db


router = Router()
database = db.Database()

# @router.message(StateFilter(None))
# async def handle_message_without_state(message: Message):
#     await message.answer("Для роботи бота введіть команду /start")
    
@router.message()
async def handle_message_without_state_none_filter(message: Message, state: FSMContext):
    current_state = await state.get_state()
    
    if current_state:
        
    
    
    await message.reply("Бот не має такої команди, спробуйте знову")
    await message.answer(str(await state.get_state()))
    