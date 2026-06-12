import asyncio
import logging
import os
import sys
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.types import Message
from queries.database import SessionLocal
from queries.model import User
from queries import config
from sqlalchemy import select
from keyboard import premium_kb, subscribe_kb
from aiogram.types import CallbackQuery


if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()

TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp["max_updates_in_flight"] = 1



@dp.message(CommandStart())
async def start_handler(message: Message):
    async with SessionLocal() as session:
        async with session.begin():
            stmt = select(User).where(
                User.id == message.from_user.id
            )
            res = await session.execute(stmt)
            user = res.scalar_one_or_none()

            if not user:
                user = User(
                    id = message.from_user.id,
                    is_bot = message.from_user.is_bot,
                    first_name = message.from_user.first_name,
                    last_name = message.from_user.last_name,
                    username = message.from_user.username,
                    language_code = message.from_user.language_code,
                    is_premium = message.from_user.is_premium
                )
                session.add(user)

            if message.from_user.is_premium:
                await message.answer(
                    f"Привет {message.from_user.first_name}! У вас Premium!",
                    reply_markup=premium_kb
                )
            else:
                await message.answer(
                    f"Привет! {message.from_user.first_name}! У вас стандартная учетная запись",
                    reply_markup=subscribe_kb
                )
                await session.commit()


#Отправка подписки
@dp.callback_query(lambda c: c.data == "get_subscribe")
async def get_subscribe(callback: CallbackQuery):
    await callback.message.answer(
        "https://crysubik.com/pU-TUFm_4F-8U3Ht"
    )
    await callback.answer()

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())