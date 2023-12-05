from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def startup_menu():
  builder = ReplyKeyboardBuilder()
  builder.row(
    types.KeyboardButton(text="Баланс по счётам"),
    types.KeyboardButton(text="Отчёты")
  )

  builder.row(
    types.KeyboardButton(text="Настройки"),
    types.KeyboardButton(text="Google-таблица")
  )

  #builder.adjust(5)

  return builder.as_markup(resize_keyboard=True)
