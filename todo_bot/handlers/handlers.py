from aiogram import types, Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.filters.callback_data import CallbackData

from keyboards import get_keyboard
from text import NEW_TASK_TEXT

router = Router()

@router.message(F.text)
async def channel_message(message: Message):
  await message.answer("Testttt")
  await message.answer(
    text="123",
    reply_markup=get_keyboard()
  )
