from aiogram import types

from aiogram.types import  InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_keyboard():
    buttons = [
      types.InlineKeyboardButton(text="-1", callback_data="num_decr"),
      types.InlineKeyboardButton(text="+1", callback_data="num_incr")
    ]
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard