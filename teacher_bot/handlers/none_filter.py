from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from database import db

from assets.classes import UserStates


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
    else:
        state_str = database.get_user_state(message.from_user.id)[1]
        print(state_str)
        state_name = state_str.split(":")[1]
        state_obj = getattr(UserStates, state_name, None)
        
        if state_obj:
            await state.set_state(state_obj)
            await message.reply("Бот аварійно завершив свою роботу. Ваш попередній стан відновлено, натисніть потрібну вам кнопку ще раз.")
            
        else:
            print(f"State '{state_name}' не найдено в UserStates.")
    