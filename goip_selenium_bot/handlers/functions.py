from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

from database import db

from assets.ussd import run_all as ussd_run
from assets.active_sims import run_all as active_run
from assets.select_1sim import run_all as change_active_run

from assets.classes import *

from config_reader import config

user = User()
    
async def background_task_ussd(callback_query, only_collect):
    try:
        await ussd_run(only_collect)
        await callback_query.message.answer("Запит усіх номерів виконано!")
    finally:
        RunAllState.runningUSSDScript = False
        
async def background_task_active(callback_query):
    try:
        await active_run()
        await callback_query.message.answer("Запит активних номерів виконано!")
    finally:
        RunAllState.runningActiveSIMS = False
        
async def background_task_change_active(callback_query, channel):
    phone = None
    try:
        phone = await change_active_run(channel)
        await callback_query.message.answer("Запит на зміну каналу виконано!")
    finally:
        RunAllState.runningChangeActiveSim = False
        
        return phone
    
def greet_user(user):
    database = db.Database()
    
    user_firstname = user.firstname
    user_name = user.firstname
    user_id = user.tg_id
    
    db_response = database.get_admin_users()
    user_ids_from_db = [record[1] for record in db_response]
    
    greet_text = "Привіт,"
    
    if user_firstname:
        greet_text += f" {user_firstname}."
    else:
        greet_text += f" {user_name}."
        
    if user_id in user_ids_from_db:
        greet_text += " Ви є адміністратором. Виберіть необхідну дію. Для перегляду можливих команд, введіть /help_admin"
        state = "state_admin_menu"
    else:
        greet_text += " Оберіть один з потрібних розділів меню. Для відкриття допомоги, введіть: /help"
        state = "state_user_menu"

    return greet_text, state

def check_admin_user(user_id):
    database = db.Database()
    db_response = database.get_admin_users()
    user_ids_from_db = [record[1] for record in db_response]
    
    state = ""
    
    if user_id in user_ids_from_db:
        state = "state_admin"
    else:
        state = "state_user"
        
    return state

def split_message(text):
    messages = []
    while len(text) > config.max_message_length:
        split_index = text.rfind('\n', 0, config.max_message_length)
        
        if split_index == -1:
            split_index = config.max_message_length

        messages.append(text[:split_index])
        
        text = text[split_index:].lstrip()
    
    messages.append(text)
    return messages

def format_number(number_str: str) -> str:
    if len(number_str) == 1:
        return f"0{number_str}" 
    return number_str  
