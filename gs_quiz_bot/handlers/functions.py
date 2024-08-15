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


class General(StatesGroup):
    test_choosing = State()
    test_theory = State()
    test_practice = State()
    
    
def greet_user(user):
    database = db.Database()
    
    user_firstname = user.firstname
    user_name = user.firstname
    
    greet_text = "Привіт,"
    
    print(database.get_admin_users())
    
    if user_firstname:
        greet_user = user_firstname
        greet_text += f" {greet_user}."
    else:
        greet_user = user_name
        greet_text += f" {user_name}."
        
    greet_text += " Для проходження тесту оберіть один з потрібних. Для відкриття допомоги, введіть: /help ."
    
    return greet_text
        
        