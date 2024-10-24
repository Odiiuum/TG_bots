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

@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    
    user_name = message.from_user.username
    user_firstname = message.from_user.first_name
    user_lastname = message.from_user.last_name
    user_id = message.from_user.id

    global user  

    user = User(user_id, user_name, user_firstname, user_lastname)
    database.add_user(user)
    
    # print(vars(user))  # Печатает все атрибуты объекта user

    greet_text, user_state  = greet_user(user)
    
    if user_state == "state_admin_menu":
        await state.set_state(AdminStates.main_menu)
    elif user_state == "state_user_menu":
        await state.set_state(UserStates.main_menu)
            
    await message.answer(greet_text, reply_markup=main_menu_kb())
    
    
@router.message(Command("get_numbers"),  StateFilter(*[value for key, value in UserStates.__dict__.items() if isinstance(value, State)]))
async def cmd_get_numbers(message: Message, state: FSMContext):
    await message.answer("У вас недостатньо прав для виконання цієї команди")    
    
@router.message(Command("get_numbers"), StateFilter(*[value for key, value in AdminStates.__dict__.items() if isinstance(value, State)]))
async def cmd_get_numbers_admin(message: Message, state: FSMContext):
    if RunAllState.runningUSSDScript:
        await message.answer("Задача вже виконується. Очікуйте її завершення.")
    else:
        await message.answer("Зробити запит без USSD?", reply_markup=get_inline_only_collect_keyboard())
        print("OK")
        await state.set_state(AdminStates.confirm_ussd)
        
@router.callback_query(F.data.in_({"yes_only", "no_only"}), AdminStates.confirm_ussd)
async def callback_confirm_action_only_collect_ussd(callback_query: CallbackQuery, state: FSMContext):
        if callback_query.data == "yes_only":
            await state.update_data(only_collect=True)
        else:
            await state.update_data(only_collect=False)
        await callback_query.answer()
        await callback_query.message.answer("Ви впевнені, що хочете продовжити?", reply_markup=get_inline_confirm_kb())
    
@router.callback_query(F.data.in_({"confirm", "cancel"}), AdminStates.confirm_ussd)
async def callback_confirm_action_ussd(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == "confirm":
        RunAllState.runningUSSDScript = True
        await callback_query.message.answer("Запуск задачі...", reply_markup=main_menu_kb())
        await callback_query.answer()
        user_data = await state.get_data()
        only_collect = user_data.get("only_collect")
        asyncio.create_task(background_task_ussd(callback_query, only_collect))
        await state.set_state(AdminStates.main_menu)
    else:
        await callback_query.message.answer("Дія скасована.", reply_markup=main_menu_kb())
        await callback_query.answer()
        await state.set_state(AdminStates.main_menu)
    
@router.message(Command("get_active"))
async def cmd_active_sim(message: Message, state: FSMContext):
    if RunAllState.runningActiveSIMS:
        await message.answer("Задача вже виконується. Очікуйте її завершення.")
    else:
        user_id = message.from_user.id
        user_state = check_admin_user(user_id)             
        if user_state == "state_admin":
            await state.set_state(AdminStates.confirm_active_sim)
        elif user_state == "state_user":
            await state.set_state(UserStates.confirm_active_sim)
            
        await message.answer("Ви впевнені, що хочете продовжити?", reply_markup=get_inline_confirm_kb())

@router.callback_query(F.data.in_({"confirm", "cancel"}), StateFilter(AdminStates.confirm_active_sim, UserStates.confirm_active_sim))
async def callback_confirm_action_active_sim(callback_query: CallbackQuery, state: FSMContext):
    if callback_query.data == "confirm":
        RunAllState.runningActiveSIMS = True
        await callback_query.message.answer("Запуск задачі...", reply_markup=main_menu_kb())
        await callback_query.answer()

        asyncio.create_task(background_task_active(callback_query))
                        
        user_id = callback_query.message.from_user.id
        user_state = check_admin_user(user_id)
        if user_state == "state_admin":
            await state.set_state(AdminStates.main_menu)
        elif user_state == "state_user":
            await state.set_state(UserStates.main_menu)
            
    else:
        await callback_query.message.answer("Дія скасована.")
        await callback_query.answer()

        user_id = callback_query.message.from_user.id
        user_state = check_admin_user(user_id)
        if user_state == "state_admin":
            await state.set_state(AdminStates.main_menu)
        elif user_state == "state_user":
            await state.set_state(UserStates.main_menu)
            

@router.message(Command("status_sim"))
async def cmd_status_sim(message: Message, state: FSMContext):
    await message.answer("status_sim")
    
@router.message(Command("help"))
async def cmd_help(message: Message, state: FSMContext):
    await message.answer(
"""/get_numbers - відправити запит усіх номерів
/get_active - відправити запит для отримання активних номерів
""")

