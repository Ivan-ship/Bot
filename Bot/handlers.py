from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from keyboard import  subscribe_kb, info_kb, devices_kb
from texts.start import get_start_text


router = Router()

@router.message(F.text == "ℹ️ Информация")
async def info(message: Message):
    print("Info")
    await message.answer(
        "Информация",
        reply_markup=info_kb
    )

@router.message(F.text == "Стандартная подписка")
async def standart(message: Message):
    await message.answer(
        "Выберите тариф:",
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

@router.callback_query(F.data == "android")
async def devices(callback: CallbackQuery):
    await callback.message.answer(
        "Скачать приложение:\n"
        "https://play.google.com/store/apps/details?id=llc.itdev.incy"
        )
    await callback.answer()

@router.callback_query(F.data == "ios")
async def devices(callback: CallbackQuery):
    await callback.message.answer(
        "Скачать приложение:\n"
        "https://apps.apple.com/app/id6746188973"
        )
    await callback.answer()


@router.callback_query(F.data == "windows")
async def devices(callback: CallbackQuery):
    await callback.message.answer(
        "Скачать приложение:\n"
        "https://github.com/Happ-proxy/happ-desktop/releases/latest/download/setup-Happ.x64.exe"
        )
    await callback.answer()


@router.callback_query(F.data == "mac")
async def devices(callback: CallbackQuery):
    await callback.message.answer(
        "Скачать приложение:\n"
        "https://github.com/Happ-proxy/happ-desktop/releases/download/2.17.1/Happ.macOS.universal.dmg"
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
    await callback.message.answer("Вы выбрали 1 месяц — 199₱")
    await callback.answer()


@router.callback_query(F.data == "month3")
async def month3(callback: CallbackQuery):
    await callback.message.answer("Вы выбрали 3 месяца — 512₱")
    await callback.answer()