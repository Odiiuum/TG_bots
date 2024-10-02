from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

from database import db

class User:
    def __init__(self, tg_id="", username="", firstname="", lastname=""):
        self.tg_id = tg_id           
        self.username = username      
        self.firstname = firstname    
        self.lastname = lastname

    def __repr__(self):
        return f"User(tg_id={self.tg_id}, username='{self.username}', firstname='{self.firstname}', lastname='{self.lastname}.')"


class AdminStates(StatesGroup):
    admin_main_menu = State()         
    admin_manage_users = State()      
    admin_view_logs = State()         

class UserStates(StatesGroup):
    user_main_menu = State()           
    user_view_results = State()     
    
class UserTestStates(StatesGroup):
    test_start = State()
    test_question = State()

    
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
        greet_text += " Для проходження тесту оберіть один з потрібних. Для відкриття допомоги, введіть: /help"
        state = "state_user_menu"

    return greet_text, state
        
        