from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from keyboard import  subscribe_kb, info_kb, devices_kb
from texts.start import get_start_text
from subscribe.subscribe import create_subscription
from queries.database import SessionLocal


router = Router()

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


@router.callback_query(F.data == "month1")
async def month1(callback: CallbackQuery):
    
    async with SessionLocal() as session:
        await create_subscription(
            session=session,
            user_id=callback.from_user.id,
            month=1,
            price = 200
        )
    await callback.message.answer("Вы выбрали 1 месяц")
    await callback.answer()


@router.callback_query(F.data == "month3")
async def month3(callback: CallbackQuery):
    await callback.message.answer("Вы выбрали 3 месяца — 512₱")
    await callback.answer()

@router.callback_query(F.data == "month6")
async def month3(callback: CallbackQuery):
    await callback.message.answer("Вы выбрали 6 месяцув — 1024₱")
    await callback.answer()