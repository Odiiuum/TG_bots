import asyncio
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.user_start_kb import *
from keyboards.admin_kb import *
from database import db
from handlers.functions import *

from assets.text_rules import rules 
from assets.classes import *

router = Router()
database = db.Database()

@router.message(F.text.lower() == "правила та компліменти") # , StateFilter(UserStates.main_menu)
async def rules_and_compliments_button(message: Message, state: FSMContext):
    await message.answer("Виберіть, що вас цікавить.", reply_markup=rules_and_compliments_menu())
    

@router.message(F.text.lower() == "правила") # , StateFilter(UserStates.main_menu)
async def rules_button(message: Message, state: FSMContext):
    await message.answer(rules, reply_markup=rules_inline_menu(), parse_mode="HTML")
    
    
@router.callback_query(F.data.in_({"confirmed_rules"}))
async def change_confirmed_rules(callback_query: CallbackQuery, state: FSMContext):
    current_markup = callback_query.message.reply_markup
    current_button = current_markup.inline_keyboard[0][0]
    is_confirmed = current_button.text.startswith("✅")
    new_markup = rules_inline_menu(confirmed=not is_confirmed)
    await callback_query.message.edit_reply_markup(reply_markup=new_markup)
    
    user_id = callback_query.from_user.id
    database.update_user_confirmed_rules(user_id, not is_confirmed)
    
    await callback_query.answer(
        "Ви ознайомились с правилами!" if not is_confirmed else "Вы відмінили підтверждення!"
    )

    
@router.message(F.text.lower() == "компліменти") # , StateFilter(UserStates.main_menu)
async def compliments_button(message: Message, state: FSMContext):
    await message.answer("Компліменти!!!!!!!!!")
    