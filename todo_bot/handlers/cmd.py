from aiogram import Router, F
from aiogram import types
from aiogram.filters import Command

from keyboards import keyboards
from text import text

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
  start_menu = await keyboards.startup_menu()
  await message.answer(text.HELLO_MESSAGE,
                   reply_markup=start_menu)
  
@router.message(Command("help"))
async def cmd_help(message: types.Message):
  await message.answer(text.HELP_CMD)
  await message.delete()