from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from middleware.registration import UserRegister
from middleware.db import DbMiddleware
from queries.model import User
from keyboard import info_kb
from texts.start import get_start_text

router = Router()

router.message.middleware(DbMiddleware())
router.callback_query.middleware(DbMiddleware())
router.message.middleware(UserRegister())
router.callback_query(UserRegister)

router.callback_query.middleware(DbMiddleware())
router.callback_query.middleware(UserRegister())

@router.message(CommandStart())
async def start_handler(message: Message, user: User):
            await message.answer(
                get_start_text(user.first_name),
                reply_markup=info_kb
            )