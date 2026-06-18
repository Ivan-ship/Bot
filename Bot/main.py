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
from handlers import info_kb
from handlers import router as subscribe_router
from texts.start import get_start_text
from queries.database import create_tables

if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()

TOKEN = os.getenv("API_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()
dp.include_router(subscribe_router)
dp["max_updates_in_flight"] = 1

@dp.message(CommandStart())
async def start_handler(message: Message):
    async with SessionLocal() as session:
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
                await session.commit()
            name = user.first_name if user else message.from_user.first_name
            await message.answer(
                get_start_text(name),
                reply_markup=info_kb
            )


async def main():
    await create_tables()
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())