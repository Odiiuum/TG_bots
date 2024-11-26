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

@router.callback_query(F.data.startswith("compliments_female"))
async def compliments_female_inline_menu_callback(callback_query: CallbackQuery, state: FSMContext):
    action = callback_query.data.split("-")[-1]

    # Словарь с текстами для тем
    topic_texts = {
        "tenderness": text_female.female_compliments_tenderness,
        "only_you": text_female.female_compliments_only_you,
        "delight": text_female.female_compliments_delight,
        "influence": text_female.female_compliments_influence,
        "funny": text_female.female_compliments_funny,
        "appearance": text_female.female_compliments_appearance,
        "character": text_female.female_compliments_character,
        "sex": text_female.female_compliments_sex,
    }

    if action in topic_texts:
        log_user_action(callback_query, f"Click for inline button 'Компліменти ЖЦА - {action.capitalize()}'.")
        
        index = list(topic_texts.keys()).index(action)
        await state.update_data(current_index=index)
        
        await callback_query.message.edit_text(topic_texts[action], reply_markup=compliments_female_inline_sub_menu())
        await callback_query.answer()

    elif action in ["submenu_next", "submenu_previous", "submenu_back"]:
        state_data = await state.get_data()
        current_index = state_data.get("current_index", 0)

        if action == "submenu_next":
            current_index = (current_index + 1) % len(topic_texts) 
            log_user_action(callback_query, "Clicked for compliments_female_inline_menu 'Next' button.")
        elif action == "submenu_previous":
            current_index = (current_index - 1) % len(topic_texts)  
            log_user_action(callback_query, "Clicked for compliments_female_inline_menu 'Previous' button.")
        elif action == "submenu_back":
            log_user_action(callback_query, "Clicked for compliments_female_inline_menu 'Back to main menu' button.")
            await callback_query.message.edit_text("Виберіть тематику компліменту.", reply_markup=compliments_female_inline_menu())
            await callback_query.answer()
            return

        await state.update_data(current_index=current_index)

        selected_topic = list(topic_texts.keys())[current_index]
        log_user_action(callback_query, f"Current compliments menu: '{selected_topic.capitalize()}'.")


        await callback_query.message.edit_text(topic_texts[selected_topic], reply_markup=compliments_female_inline_sub_menu())
        await callback_query.answer()
    else:
        await callback_query.answer("Невідома дія.", show_alert=True)

        
        
# @router.callback_query(F.data.startswith("compliments_female_submenu_"))
# async def compliments_female_inline_sub_menu_callback(callback_query: CallbackQuery, state: FSMContext):
#     current_index = await state.get_data().get("current_index", 0)
    
#     if callback_query.data == "compliments_female_submenu_next":
#         current_index = (current_index + 1) % len(text_female.female_compliments)
#     elif callback_query.data == "compliments_female_submenu_previous":
#         current_index = (current_index - 1) % len(text_female.female_compliments)  # Переход к предыдущему элементу
#     elif callback_query.data == "compliments_female_submenu_back":
#         await callback_query.message.edit_text("Виберіть тематику компліменту.", reply_markup=compliments_female_inline_menu())
#         await callback_query.answer()
#         return
        
    