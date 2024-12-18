from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

class User:
    def __init__(self, user_id="", username="", firstname="", lastname=""):
        self.user_id = user_id           
        self.username = username      
        self.firstname = firstname    
        self.lastname = lastname

    def __repr__(self):
        return f"User(tg_id={self.user_id}, username='{self.username}', firstname='{self.firstname}', lastname='{self.lastname}.')"


# class AdminStates(StatesGroup):
    

class UserStates(StatesGroup):
    main_menu = State()
    rules_and_compliments_menu = State()
    exam_menu = State()
    
    # main_menu = State()
    # main_menu = State()
    # main_menu = State()
    
