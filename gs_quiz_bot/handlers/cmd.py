from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.user_start_kb import get_start_kb
from database import db
from handlers.functions import *

router = Router()
database = db.Database()
user = User()

@router.message(Command("start"))
async def cmd_start(message: Message):
    
    user_name = message.from_user.username
    user_firstname = message.from_user.first_name
    user_lastname = message.from_user.last_name
    user_id = message.from_user.id
        
    user = User(user_id, user_name, user_firstname, user_lastname)
    database.add_user(user)
    
    greet_text, state = greet_user(user)
            
    await message.answer(greet_text, reply_markup=get_start_kb())
    
@router.message(Command("help"))
async def cmd_help(message: Message):
    await message.answer("HELP")

