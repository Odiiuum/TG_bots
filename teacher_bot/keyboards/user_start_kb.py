from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def main_menu_kb() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Правила та компліменти")
    kb.button(text="Інструменти")
    kb.button(text="Іспит")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)

def instrument_inline_menu() -> InlineKeyboardMarkup:    
    round_robot_bot_button = InlineKeyboardButton(text="Відео-гурток", url="https://t.me/Round_Robot")
    save_as_bot_button = InlineKeyboardButton(text="Завантаження фото Inst/Pinterest", url="https://t.me/SaveAsBot")
    gtp_bot_button = InlineKeyboardButton(text="AI gpt4", url="https://t.me/gpt4bot")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[round_robot_bot_button, save_as_bot_button, gtp_bot_button]])
    
    return keyboard

def rules_and_compliments_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Правила")
    kb.button(text="Компліменти")
    kb.button(text="Повернутись")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
    
    
def compliments_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="ЖЦА")
    kb.button(text="МЦА")
    kb.button(text="Повернутись")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
    
def rules_inline_menu(confirmed: bool = False) -> InlineKeyboardMarkup:
    button_text = "✅ Ознайомлений(-а)" if confirmed else "Ознайомлен(-а)"
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=button_text, callback_data="confirmed_rules")]
        ]
    )
    return markup