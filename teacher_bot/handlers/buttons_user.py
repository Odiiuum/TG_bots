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

from assets.classes import *

from utils.logger import log_user_action

router = Router()
database = db.Database()

@router.message(F.text.lower() == "інструменти", StateFilter(UserStates.main_menu)) 
async def rules_and_compliments_button(message: Message, state: FSMContext):
    log_user_action(message, "Click for button 'Інструменти'.")
        
    data = await state.get_data()
    previous_message_id = data.get("intstruments_message_id")
    if previous_message_id:
        try:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=previous_message_id)
        except Exception as e:
            print(f"Error delete message: {e}")

    sent_message = await message.answer(
        "Інструменти, які можуть вам знадобитись.",
        reply_markup=instrument_inline_menu()
    )
    
    state.update_data(intstruments_message_id=sent_message.message_id)
    
    

@router.message(F.text.lower() == "правила та компліменти", StateFilter(UserStates.main_menu)) 
async def rules_and_compliments_button(message: Message, state: FSMContext):
    log_user_action(message, "Click for button 'Правила та компліменти'.")
    await state.set_state(UserStates.rules_and_compliments_menu)
    database.update_user_state(message.from_user.id, await state.get_state())
    
    await message.answer("Виберіть, що вас цікавить.", reply_markup=rules_and_compliments_menu())
    

@router.message(F.text.lower() == "правила", StateFilter(UserStates.rules_and_compliments_menu)) 
async def rules_button(message: Message, state: FSMContext):
    log_user_action(message, "Click for button 'Правила'.")
    
    rules = database.get_last_rule()
    
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
    
    
@router.callback_query(F.data.in_({"confirmed_rules"}))
async def change_confirmed_rules(callback_query: CallbackQuery, state: FSMContext):
    user_id = callback_query.from_user.id
    is_confirmed = database.get_user_confirmed_rules(user_id)
    
    if is_confirmed == "True":
        new_status = "False"
        action = "Unconfirmed rules."
        callback_answer = "Вы відмінили підтверждення!"
    elif is_confirmed == "False":
        new_status = "True"
        action = "Confirmed rules."
        callback_answer = "Ви ознайомились с правилами"
        
    database.update_user_confirmed_rules(user_id, new_status)  
    
    new_markup = rules_inline_menu(confirmed=new_status)
    await callback_query.message.edit_reply_markup(reply_markup=new_markup)
    
    log_user_action(callback_query, action)
    
    await callback_query.answer(callback_answer)

    
@router.message(F.text.lower() == "компліменти", StateFilter(UserStates.rules_and_compliments_menu)) 
async def compliments_button(message: Message, state: FSMContext):
    log_user_action(message, "Click for reply button 'Компліменти'.")
    await message.answer("Виберіть вашу цільову аудиторію.", reply_markup=compliments_menu())
    
    
    
@router.message(F.text.lower() == "жца") 
async def compliments_female_button(message: Message, state: FSMContext):
    log_user_action(message, "Click for reply button 'Компліменти ЖЦА'.")
    await message.answer("Виберіть тематику компліменту.", reply_markup=compliments_female_inline_menu()) #next callback in compliments_female
    
    
