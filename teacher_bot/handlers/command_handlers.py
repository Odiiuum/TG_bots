import asyncio
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.user_start_kb import *
from keyboards.admin_kb import *
from database import db
from utils.functions import *
from utils.logger import log_user_action

from assets.classes import *

router = Router()
database = db.Database()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(UserStates.main_menu)
    
    log_user_action(message, "Run \'/start\' command.")
    
    user_name = message.from_user.username
    user_firstname = message.from_user.first_name
    user_lastname = message.from_user.last_name
    user_id = message.from_user.id

    global user  

    user = User(user_id, user_name, user_firstname, user_lastname)
    database.add_user(user)
    
    greet_text = greet_user(user)
    
    admin_state = check_admin_user(user.user_id)
    
    if admin_state:
        greet_text += " Ви маєте права адміністратора. Для переходу в режим адміністрування, введіть команду /admin_menu. Якщо вам потрібна допомога, введіть /help_admin"
    else:
        greet_text += " Для відкриття допомоги напишіть /help"
        
    await message.answer(greet_text, reply_markup=main_menu_kb())
    
# @router.message(Command("start"))

        
