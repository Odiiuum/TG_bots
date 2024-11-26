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

from assets.text_rules import rules 
from assets.classes import *

from utils.logger import log_user_action

router = Router()
database = db.Database()

@router.message(F.text.lower() == "правила та компліменти") 
async def rules_and_compliments_button(message: Message, state: FSMContext):
    log_user_action(message, "Click for button 'Правила та компліменти'.")
    await message.answer("Виберіть, що вас цікавить.", reply_markup=rules_and_compliments_menu())
    

@router.message(F.text.lower() == "правила") 
async def rules_button(message: Message, state: FSMContext):
    log_user_action(message, "Click for button 'Правила'.")
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
    
    action = "Confirmed rules." if not is_confirmed else "Uncorfirmed rules."
    
    log_user_action(callback_query, action)
    
    await callback_query.answer(
        "Ви ознайомились с правилами!" if not is_confirmed else "Вы відмінили підтверждення!"
    )

    
@router.message(F.text.lower() == "компліменти") 
async def compliments_button(message: Message, state: FSMContext):
    log_user_action(message, "Click for reply button 'Компліменти'.")
    await message.answer("Виберіть вашу цільову аудиторію.", reply_markup=compliments_menu())
    
    
    
@router.message(F.text.lower() == "жца") 
async def compliments_female_button(message: Message, state: FSMContext):
    log_user_action(message, "Click for reply button 'Компліменти ЖЦА'.")
    await message.answer("Виберіть тематику компліменту.", reply_markup=compliments_female_inline_menu())
    
    
