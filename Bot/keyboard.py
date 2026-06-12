from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

premium_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="⭐ Premium функция")],
        [KeyboardButton(text="Без премиум")]
    ],
    resize_keyboard=True
)


subscribe_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(
            text="Получить подписку",
            callback_data="get_subscribe",
            style="success"
            )]
    ]
)