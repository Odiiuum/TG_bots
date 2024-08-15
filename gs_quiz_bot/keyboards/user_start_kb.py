from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Теорія")
    kb.button(text="Практика")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
