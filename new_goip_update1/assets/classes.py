from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import StateFilter

class User:
    def __init__(self, tg_id="", username="", firstname="", lastname=""):
        self.tg_id = tg_id           
        self.username = username      
        self.firstname = firstname    
        self.lastname = lastname

    def __repr__(self):
        return f"User(tg_id={self.tg_id}, username='{self.username}', firstname='{self.firstname}', lastname='{self.lastname}.')"


class AdminStates(StatesGroup):
    main_menu = State()         
    manage_users = State()      
    confirm_ussd = State()      
    confirm_active_sim = State()      
    view_logs = State()         

class UserStates(StatesGroup):
    main_menu = State()           
    confirm_active_sim = State()     
    
class ChangeActive(StatesGroup):
    first_step = State()
    second_step = State()
    confirm_step = State()
    
class RunAllState:
    runningUSSDScript = False
    runningActiveSIMS = False
    runningChangeActiveSim = False
    
