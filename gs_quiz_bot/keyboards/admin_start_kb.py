from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_start_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Питання тесту 'Теорія'")
    kb.button(text="Питання тесту 'Практика'")
    kb.button(text="Додати адміністратора")
    # kb.button(text="Додати адміністратора")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
