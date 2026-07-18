from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboard import admin_kb, about_user_kb
from states.admin_state import AdminState
from repositories.stats_repository import AdminRepositories
from repositories.user_repository import UserRepo
from repositories.keys_repository import KeyRepository
from middleware.db import DbMiddleware
from middleware.registration import UserRegister


router = Router()
router.message.middleware(DbMiddleware())
router.message.middleware(UserRegister())
router.callback_query.middleware(DbMiddleware())
router.callback_query.middleware(UserRegister())



#Admin panel
@router.message(Command("admin"))
async def admin(message: Message, user):
    if not user.is_admin:
        await message.answer("⛔ У вас нет доступа.")
        return
    else:
        await message.answer(
            "Добро пожаловать в Admin панель",
            reply_markup=admin_kb
        )

@router.callback_query(F.data == "statistics")
async def statistics(callback: CallbackQuery, session):
    repo = AdminRepositories(session)
    stats = await repo.get_statistics()
    
    await callback.message.answer(
        f"👥 Всего пользователей: {stats["user_count"]}\n"
        f"🆕 Новых сегодня: {stats["today_user_count"]}\n"
        f"🔑 Всего ключей: {stats["vless_url_count"]}\n"
        f"🟢 Активных ключей: {stats["active_vless_url"]}\n"
        f"🔴 Просроченных: {stats["disacrive_vless_url"]}" 
    )
    await callback.answer()


#About user
@router.callback_query(F.data == "users")
async def about_user(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminState.waiting_tg_id)
    await callback.message.answer("Введите telegram id пользователя!")
    await callback.answer()


@router.message(AdminState.waiting_tg_id)
async def get_user_by_tg_id(message: Message, state: FSMContext, session):
    try:
        telegram_id = int(message.text)
    except ValueError:
        await message.answer("❌ ID должен быть числовым")
        return

    repo = UserRepo(session)
    user = await repo.get_by_telegram_id(telegram_id)
    
    if user is None:
        await message.answer("Данного пользователя не существует")
        await state.clear()
        return
    
    await state.update_data(user_id = user.id)
    
    await message.answer(
        f"""
👤 Пользователь
telegramID: {user.id}
first_name: {user.first_name}
last_name: {user.last_name}
username: @{user.username}
        """,
        reply_markup=about_user_kb
    )


#Sub info
@router.callback_query(F.data == "keys")
async def key(callback: CallbackQuery, state: FSMContext, session):

    data = await state.get_data()
    user_id = data.get("user_id")
    repo = KeyRepository(session)
    sub = await repo.get_user_key(user_id)


    if sub is None:
        await callback.message.answer("❌ У данного пользователя нет активной подписки.")
        await callback.answer()
        return
    

    await callback.message.answer(
        f"""
📅 Дата покупки: {sub.start_date}
📅 Дата окончания: {sub.end_date}
🔑 Ключ:
<blockquote>{sub.url}</blockquote>
        """,
        parse_mode="HTML"
    )
    await state.clear()
    await callback.answer()
