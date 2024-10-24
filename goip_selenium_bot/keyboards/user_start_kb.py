from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def main_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Активні SIM")
    kb.button(text="Зміна активної SIM")
    kb.button(text="Показати усі номери")
    kb.button(text="Додаткове меню")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def get_inline_confirm_kb() -> InlineKeyboardMarkup:
    confirm_button = InlineKeyboardButton(text="Підтвердити", callback_data="confirm")
    cancel_button = InlineKeyboardButton(text="Відміна", callback_data="cancel")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[confirm_button, cancel_button]])
    
    return keyboard

def get_inline_only_collect_keyboard() -> InlineKeyboardMarkup:
    confirm_button = InlineKeyboardButton(text="Так", callback_data="yes_only")
    cancel_button = InlineKeyboardButton(text="Ні", callback_data="no_only")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[confirm_button, cancel_button]])
    
    return keyboard

def get_channel_sim_inline_1_keyboard():
    keyboard = []

    buttons = [InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in range(1, 17)]
    
    for i in range(0, len(buttons), 4):
        keyboard.append(buttons[i:i + 4])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_channel_sim_inline_2_keyboard():
    keyboard = []

    buttons = [InlineKeyboardButton(text=str(i), callback_data=str(i)) for i in range(1, 33)]
    
    for i in range(0, len(buttons), 4):
        keyboard.append(buttons[i:i + 4])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)