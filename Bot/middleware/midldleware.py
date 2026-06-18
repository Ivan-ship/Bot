from aiogram import BaseMiddleware
from sqlalchemy import select
from queries.model import Subscribe, User
from queries.database import SessionLocal

async def get_subscription(session, user_id: int):
    stmt = select(Subscribe).where(Subscribe.id == user_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()

class SubscribeMiddleWare(BaseMiddleware):
    async def __call__(
        self,
        handler,
        event,
        data
    ):
        async with SessionLocal() as session:
            user_id = event.from_user.id

            user_stmp = select(User).where(User.id == user_id)
            user = (await session.execute(user_stmp)).scalar_one_or_none()
            sub_stmp = select(Subscribe).where(Subscribe.id == user_id)
            sub = (await session.execute(sub_stmp)).scalar_one_or_none()
        
        data["user"] = user
        data["subscription"] = sub
        data["has_subscription"] = sub is not None and user is not None

        return await handler(event, data)