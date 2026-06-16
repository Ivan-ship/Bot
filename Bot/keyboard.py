from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

info_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="ℹ️ Информация", callback_data="info"),
            InlineKeyboardButton(text="💲Цены", callback_data="price"),
        ]
    ]
)

devices_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Android",
                url="https://play.google.com/store/apps/details?id=llc.itdev.incy"
                ),
            InlineKeyboardButton(
                text="IOS",
                url="https://apps.apple.com/app/id6746188973"
                ),   
        ],
        [
            InlineKeyboardButton(
                text="Windows",
                url="https://github.com/Happ-proxy/happ-desktop/releases/latest/download/setup-Happ.x64.exe"
                ),
            InlineKeyboardButton(
                text="MacOs",
                url="https://github.com/Happ-proxy/happ-desktop/releases/download/2.17.1/Happ.macOS.universal.dmg"
                ),
        ],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
    ]
)
subscribe_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="1 месяца: 200₱", callback_data="month1")],
        [InlineKeyboardButton(text="3 месяца: 512₱", callback_data="month3")],
        [InlineKeyboardButton(text="6 месяцев: 1024₱", callback_data="month6")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")],
    ]
)