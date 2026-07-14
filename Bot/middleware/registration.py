from aiogram import BaseMiddleware
from queries.model import User
from sqlalchemy import select
from datetime import datetime



class UserRegister(BaseMiddleware):
    async def __call__(self, handler, event, data):
            session = data["session"]

            tg_user = event.from_user

            stmt = select(User).where(User.id == tg_user.id)
            res = await session.execute(stmt)
            user = res.scalar_one_or_none()

            if user is None:
                user = User(
                    id = tg_user.id,
                    is_bot = tg_user.is_bot,
                    first_name = tg_user.first_name,
                    last_name = tg_user.last_name,
                    username = tg_user.username,
                    language_code = tg_user.language_code,
                    is_premium = tg_user.is_premium,
                    created_at = datetime.now()
                )
                session.add(user)
                await session.commit()
            
            data["user"] = user
            return await handler(event, data)