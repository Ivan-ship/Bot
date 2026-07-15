from aiogram import F,  Router
from aiogram.types import Message, CallbackQuery
from middleware.midldleware import SubscribeMiddleWare
from subscribe.subscribe import create_subscription
from middleware.db import DbMiddleware

router = Router()
router.message.middleware(DbMiddleware())
router.message.middleware(SubscribeMiddleWare())
router.callback_query.middleware(DbMiddleware())
router.callback_query.middleware(SubscribeMiddleWare())


@router.callback_query(F.data == "month1")
async def month1(
    callback: CallbackQuery,
    has_subscription: bool,
    subscription,
    session
    ):
    
    if has_subscription:
        await callback.message.answer(
            f"У вас уже активная подписка до: {subscription.end_date}"
        )
        await callback.answer()
        return


    sub = await create_subscription(
        session=session,
        user_id=callback.from_user.id,
        month=1,
        price = 200,
        plan = "Тариф: 1 месяц"
        )
    await callback.message.answer(
        f"Вы выбрали 1 месяц, ваша подписка: \n"
        f"<blockquote>{sub.url}</blockquote>",
        parse_mode="HTML"
        )
    await callback.answer()


@router.callback_query(F.data == "month3")
async def month3(
    callback: CallbackQuery,
    has_subscription: bool,
    subscription,
    session
    ):

    if has_subscription:
        await callback.message.answer(
            f"У вас уже активная подписка до: {subscription.end_date}"
        )
        await callback.answer()
        return


    sub = await create_subscription(
        session=session,
        user_id=callback.from_user.id,
        month=3,
        price = 512,
        plan = "Тариф: 3 месяца"
        )

    await callback.message.answer(
        f"Вы выбрали 3 месяца, ваша подписка: \n"
        f"<blockquote>{sub.url}</blockquote>",
        parse_mode="HTML"
        )
    await callback.answer()


@router.callback_query(F.data == "month6")
async def month3(
    callback: CallbackQuery,
    has_subscription: bool,
    subscription,
    session
    ):

    if has_subscription:
        await callback.message.answer(
            f"У вас уже активная подписка до: {subscription.end_date}"
        )
        await callback.answer()
        return

    sub = await create_subscription(
        session=session,
        user_id=callback.from_user.id,
        month=6,
        price = 1024,
        plan = "Тариф: 6 месяцев"
        )

    await callback.message.answer(
        f"Вы выбрали 6 месяцев, ваша подписка: \n"
        f"<blockquote>{sub.url}</blockquote>",
        parse_mode="HTML"
        )
    await callback.answer()