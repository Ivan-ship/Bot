from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from keyboard import  subscribe_kb, info_kb, devices_kb
from texts.start import get_start_text
from subscribe.subscribe import create_subscription
from queries.database import SessionLocal
from middleware.midldleware import SubscribeMiddleWare, get_subscription


router = Router()
router.message.middleware(SubscribeMiddleWare())
router.callback_query.middleware(SubscribeMiddleWare())

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
async def month1(
    callback: CallbackQuery,
    has_subscription: bool,
    subscription
    ):
    
    async with SessionLocal() as session:

        if has_subscription:
            await callback.message.answer(
                f"У вас уже активная подписка до: {subscription.end_date}"
            )
            await callback.answer()
            return

        async with SessionLocal() as session:
            sub = await create_subscription(
                session=session,
                user_id=callback.from_user.id,
                month=1,
                price = 200,
                plan = "Тариф: 1 месяц"
            )
    await callback.message.answer(
        f"Вы выбрали 1 месяц, ваша подписка: \n"
        f"Ваша ссылка: {sub.url}"
        )
    await callback.answer()


@router.callback_query(F.data == "month3")
async def month3(
    callback: CallbackQuery,
    has_subscription: bool,
    subscription
    ):

    async with SessionLocal() as session:

        if has_subscription:
            await callback.message.answer(
                f"У вас уже активная подписка до: {subscription.end_date}"
            )
            await callback.answer()
            return

        async with SessionLocal() as session:
            sub = await create_subscription(
                session=session,
                user_id=callback.from_user.id,
                month=3,
                price = 512,
                plan = "Тариф: 3 месяца"
            )

    await callback.message.answer(
        f"Вы выбрали 3 месяца, ваша подписка: \n"
        f"Ваша ссылка: {sub.url}"
        )
    await callback.answer()

    await callback.message.answer("Вы выбрали 3 месяца — 512₱")
    await callback.answer()

@router.callback_query(F.data == "month6")
async def month3(
    callback: CallbackQuery,
    has_subscription: bool,
    subscription
    ):
    
    async with SessionLocal() as session:

        if has_subscription:
            await callback.message.answer(
                f"У вас уже активная подписка до: {subscription.end_date}"
            )
            await callback.answer()
            return

        async with SessionLocal() as session:
            sub = await create_subscription(
                session=session,
                user_id=callback.from_user.id,
                month=6,
                price = 1024,
                plan = "Тариф: 6 месяцев"
            )

    await callback.message.answer(
        f"Вы выбрали 6 месяцев, ваша подписка: \n"
        f"Ваша ссылка: {sub.url}"
        )
    await callback.answer()

    await callback.message.answer("Вы выбрали 6 месяцев — 1024₱")
    await callback.answer()


#account info
@router.callback_query(F.data == "account")
async def about_user(callback: CallbackQuery):
    async with SessionLocal() as session:
        sub = await get_subscription(session, callback.from_user.id)

        text = f"👤 Аккаунт: {callback.from_user.id}\n"

        if sub:
            text += f"📅 Подписка активна до: {sub.end_date}\n"
            text += f"Ваша ссылка: {sub.url}\n"
            text += f"{sub.plan}"
        else:
            text += "❌ У вас нет активной подписки"

    await callback.message.answer(text)
    await callback.answer()
 
    
    await callback.message.answer()
