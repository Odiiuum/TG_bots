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

from assets.text_rules import rules 


router = Router()
database = db.Database()

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await state.set_state(UserStates.main_menu)
    current_state = await state.get_state()
    
    log_user_action(message, "Run \'/start\' command.")
    
    user_name = message.from_user.username
    user_firstname = message.from_user.first_name
    user_lastname = message.from_user.last_name
    user_id = message.from_user.id
        
    global user  

    user = User(user_id, user_name, user_firstname, user_lastname)
    database.add_user(user)
    database.update_user_state(user_id, current_state)
    
    greet_text = greet_user(user)
    
    admin_state = check_admin_user(user.user_id)
    
    if admin_state:
        greet_text += " Ви маєте права адміністратора. Для переходу в режим адміністрування, введіть команду /admin_menu. Якщо вам потрібна допомога, введіть /help_admin"
    else:
        greet_text += " Для відкриття допомоги напишіть /help"
        
    await message.answer(greet_text, reply_markup=main_menu_kb())
    
    
@router.message(Command("rules")) 
async def cmd_rules(message: Message, state: FSMContext):
    log_user_action(message, "Click for button 'Правила'.")
    data = await state.get_data()
    previous_message_id = data.get("rules_message_id")
    if previous_message_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=previous_message_id)
        except Exception as e:
            print(f"Error delete message: {e}")

    user_id = message.from_user.id
    is_confirmed = database.get_user_confirmed_rules(user_id)

    sent_message = await message.answer(
        rules,
        reply_markup=rules_inline_menu(is_confirmed),
        parse_mode="HTML"
    )
    
    await state.update_data(rules_message_id=sent_message.message_id)
    
    
@router.message(Command("state")) 
async def cmd_state(message: Message, state: FSMContext):
    
    user_state = list_to_text(database.get_compliments_female())
    await message.answer(user_state)
        
