from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

info_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="ℹ️ Информация", callback_data="info")]
    ]
)

devices_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Android", callback_data="android"),
            InlineKeyboardButton(text="IOS", callback_data="ios"),
            
        ],
        [
            InlineKeyboardButton(text="Windows", callback_data="windows"),
            InlineKeyboardButton(text="MacOs", callback_data="mac"),
        ],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
    ]
)

subscribe_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="1 месяца: 200₱", callback_data="month1")],
        [InlineKeyboardButton(text="3 месяца: 512₱", callback_data="month3")],
    ]
)