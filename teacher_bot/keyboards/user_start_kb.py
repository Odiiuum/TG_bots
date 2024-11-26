from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from assets import text_female #, text_male


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
    kb.button(text="Повернутись 🔙")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)
    
    
def compliments_menu() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="ЖЦА")
    kb.button(text="МЦА")
    kb.button(text="Повернутись 🔙")
    kb.adjust(2)
    return kb.as_markup(resize_keyboard=True)


def compliments_female_inline_menu() -> InlineKeyboardMarkup:
    female_compliments_tenderness = InlineKeyboardButton(text="Ніжність", callback_data="compliments_female-tenderness")
    female_compliments_only_you = InlineKeyboardButton(text="Саме ти", callback_data="compliments_female-only_you")
    female_compliments_delight = InlineKeyboardButton(text="Захоплення", callback_data="compliments_female-delight")
    female_compliments_influence = InlineKeyboardButton(text="Її вплив на тебе", callback_data="compliments_female-influence")
    female_compliments_funny = InlineKeyboardButton(text="Жартівливі", callback_data="compliments_female-funny")
    female_compliments_appearance = InlineKeyboardButton(text="Зовнішність фото/відео", callback_data="compliments_female-appearance")
    female_compliments_character = InlineKeyboardButton(text="Характер", callback_data="compliments_female-character")
    female_compliments_sex = InlineKeyboardButton(text="Сексуальність", callback_data="compliments_female-sex")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        female_compliments_tenderness,
        female_compliments_only_you,
    ],
    [
        female_compliments_delight,
        female_compliments_influence,
    ],
    [
        female_compliments_funny,
        female_compliments_appearance,
    ],
    [
        female_compliments_character,
        female_compliments_sex
    ]])
    
    return keyboard


def compliments_female_inline_sub_menu() -> InlineKeyboardMarkup:
    next_button = InlineKeyboardButton(text="Наступний", callback_data="compliments_female-submenu_next")
    previous_button = InlineKeyboardButton(text="Попередній", callback_data="compliments_female-submenu_previous")
    back_button = InlineKeyboardButton(text="Повернутися в меню", callback_data="compliments_female-submenu_back")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        previous_button,
        next_button
    ],
    [
        back_button
    ]])
    
    return keyboard
    
    
def rules_inline_menu(confirmed: bool = False) -> InlineKeyboardMarkup:
    button_text = "✅ Ознайомлений(-а)" if confirmed else "Ознайомлен(-а)"
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=button_text, callback_data="confirmed_rules")]
        ]
    )
    return markup


def compliments_male_inline_menu() -> InlineKeyboardMarkup:
    male_compliments_appearance = InlineKeyboardButton(text="Зовнішність фото/відео", callback_data="compliments_male-appearance")
    male_compliments_only_you = InlineKeyboardButton(text="Саме ти", callback_data="compliments_male-only_you")
    male_compliments_character = InlineKeyboardButton(text="Характер", callback_data="compliments_male-character")
    male_compliments_sex = InlineKeyboardButton(text="Сексуальність", callback_data="compliments_male-sex")
    male_compliments_funny = InlineKeyboardButton(text="Жартівливі", callback_data="compliments_male-funny")
    
    male_compliments_methodology = InlineKeyboardButton(text="Методології комунікації", callback_data="compliments_male-methodology")
    male_compliments_anchor = InlineKeyboardButton(text="", callback_data="compliments_male-anchor")
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[[
        male_compliments_only_you,
        male_compliments_sex     
    ],
    [
        male_compliments_funny,
        male_compliments_appearance,
    ],
    [
        male_compliments_character
    ],
    [
        male_compliments_methodology,
        male_compliments_anchor
    ]
    ])
    
    return keyboard