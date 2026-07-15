from aiogram import F,  Router
from aiogram.types import Message, CallbackQuery
from keyboard import info_kb, subscribe_kb, devices_kb
from texts.start import get_start_text
from middleware.midldleware import get_subscription
from middleware.db import DbMiddleware 

router = Router()
router.message.middleware(DbMiddleware())
router.callback_query.middleware(DbMiddleware())

@router.message(F.text == "ℹ️ Информация")
async def info(message: Message):
    print("Info")
    await message.answer(
        "Информация",
        reply_markup=info_kb
    )

#Price
@router.callback_query(F.data == "price")
async def subscribe_price(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите тариф",
        reply_markup=subscribe_kb
    )



#Devices
@router.callback_query(F.data == "info")
async def info_callback(callback: CallbackQuery):
    await callback.message.edit_text(
        "Выберите устройство",
        reply_markup=devices_kb
        )
    await callback.answer()

#Callback back
@router.callback_query(F.data == "back")
async def back_main(callback: CallbackQuery):
    await callback.message.edit_text(
        get_start_text(callback.from_user.first_name),
        reply_markup=info_kb
    )


#account info
@router.callback_query(F.data == "account")
async def about_user(callback: CallbackQuery, session):
    sub = await get_subscription(session, callback.from_user.id)
    text = f"👤 Аккаунт: {callback.from_user.id}\n"

    if sub:
        text += f"📅 Подписка активна до: {sub.end_date}\n"
        text += f"Ваша ссылка: \n"
        text += f"<blockquote>{sub.url}</blockquote>"
        text += f"{sub.plan}"
    else:
        text += "❌ У вас нет активной подписки"

    await callback.message.answer(text, parse_mode="HTML")
    await callback.answer()
