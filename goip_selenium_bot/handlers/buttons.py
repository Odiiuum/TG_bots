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

from assets.classes import *

router = Router()
database = db.Database()

@router.message(F.text.lower() == "показати усі номери")
async def get_all_phone(message: Message, state: FSMContext):
    all_numbers = database.get_all_numbers()
    
    if not all_numbers:
        await message.answer("База даних ще не містить жодного номеру. Повторіть запит /get_numbers та спробуйте знову.")
        return 

    formatted_numbers_phone = '\n'.join([f"{slot}: {phone}" for _, slot, phone in all_numbers])
    messages = split_message(formatted_numbers_phone)
    
    for msg in messages:
        await message.answer(msg)
        
@router.message(F.text.lower() == "активні sim")
async def get_all_phone(message: Message, state: FSMContext):
    all_numbers = database.get_active_numbers()
    
    await message.answer("Активні слоти можуть бути неактуальні, для оновлення даних повторіть запит /get_active")
    
    if not all_numbers:
        await message.answer("База даних ще не містить жодного номеру. Повторіть запит /get_active та спробуйте знову.")
        return 

    formatted_numbers_phone = '\n'.join([f"{slot}: {phone}" for _, slot, phone in all_numbers])
    await message.answer(formatted_numbers_phone)

@router.message(F.text.lower() == "зміна активної sim")
async def change_active_sim(message: Message, state: FSMContext):
    if RunAllState.runningChangeActiveSim:
        await message.answer("Задача вже виконується. Очікуйте її завершення.")
    else:
        await message.answer("Виберіть необхідний слот. В один момент часу активними можуть бути тільки 16 SIM", reply_markup=get_channel_sim_inline_1_keyboard())
        await state.set_state(ChangeActive.first_step)
        
@router.callback_query(StateFilter(ChangeActive.first_step))
async def process_first_slot_selection(callback_query: CallbackQuery, state: FSMContext):
    selected_slot = callback_query.data
    await state.update_data(first_slot=selected_slot)
    
    await callback_query.message.edit_text("Виберіть другий слот для активації:", 
                                           reply_markup=get_channel_sim_inline_2_keyboard())
    await callback_query.answer() 
    await state.set_state(ChangeActive.second_step)
    
@router.callback_query(StateFilter(ChangeActive.second_step))
async def process_second_slot_selection(callback_query: CallbackQuery, state: FSMContext):
    second_slot = callback_query.data
    user_data = await state.get_data()
    
    first_slot = user_data.get("first_slot")
    
    slot = first_slot + "." + format_number(second_slot)
    
    await state.update_data(slot=slot)
    
    await callback_query.message.answer(f"Вибраний слот для активації: {slot}", reply_markup=get_inline_confirm_kb())
    await callback_query.answer()
    
    await state.set_state(ChangeActive.confirm_step)
    
@router.callback_query(StateFilter(ChangeActive.confirm_step))
async def process_second_slot_selection(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == "confirm":
        RunAllState.runningChangeActiveSim = True
        await callback_query.message.answer("Запуск задачі...", reply_markup=main_menu_kb())
        await callback_query.answer()
        
        user_data = await state.get_data()
        
        slot = user_data.get("slot")
        
        async def task_with_result(callback_query: CallbackQuery, slot: str):
            result_text = await background_task_change_active(callback_query, slot)
            await callback_query.message.answer(f"{slot}: {result_text}")
            # print("slot:", slot)
            # print("DATA:", result_text)
            database.update_number_active(str(slot), str(result_text))
            
        asyncio.create_task(task_with_result(callback_query, slot))
        
        user_id = callback_query.message.from_user.id
        user_state = check_admin_user(user_id)
        if user_state == "state_admin":
            await state.set_state(AdminStates.main_menu)
        elif user_state == "state_user":
            await state.set_state(UserStates.main_menu)
    
    else:
        await callback_query.message.answer("Дія скасована.")
        await callback_query.answer()
        
        user_state = check_admin_user(user)
        if user_state == "state_admin":
            await state.set_state(AdminStates.main_menu)
        elif user_state == "state_user":
            await state.set_state(UserStates.main_menu)
            
@router.message(F.text.lower() == "додаткове меню")
async def other_menu(message: Message, state: FSMContext):
    # database.update_number_active("1.32", "+38099999999")
    message.answer("Це меню ще не доступне.")
    