from aiogram import BaseMiddleware
from sqlalchemy import select
from queries.model import Subscribe, User
from queries.database import SessionLocal
from datetime import date

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

            user = (
                await session.execute(select(User).where(User.id == user_id))
            ).scalar_one_or_none()

            sub = (
                await session.execute(select(Subscribe).where(Subscribe.id == user_id))
            ).scalar_one_or_none()

            has_subscription = (
                user is not None and sub is not None and sub.is_active and  sub.end_date >= date.today()
            )

        data["user"] = user
        data["subscription"] = sub
        data["has_subscription"] = has_subscription

        return await handler(event, data)