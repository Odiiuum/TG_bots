from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

from database import db

from assets.classes import *

from config_reader import config

user = User()
        
def greet_user(user):    
    user_firstname = user.firstname
    user_name = user.firstname
    
    greet_text = "Привіт,"
    
    if user_firstname:
        greet_text += f" {user_firstname}."
    else:
        greet_text += f" {user_name}."
        
    return greet_text

def check_admin_user(user_id):
    database = db.Database()
    db_response = database.get_admin_users()
    user_ids_from_db = [record[1] for record in db_response]
       
    if user_id in user_ids_from_db:
        state = True
    else:
        state = False
        
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
