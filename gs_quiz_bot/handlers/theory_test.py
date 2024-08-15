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



@router.message(F.text.lower() == "теорія")
async def start_test_theory(message: Message):
    print(database.get_questions("questions_theory"))