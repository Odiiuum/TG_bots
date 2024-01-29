from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def startup_menu():
  builder = ReplyKeyboardBuilder()
  builder.row(

  )

  builder.row(

  )

  #builder.adjust(5)

  return builder.as_markup(resize_keyboard=True)
