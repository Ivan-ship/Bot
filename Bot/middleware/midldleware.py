from aiogram import BaseMiddleware
from sqlalchemy import select
from queries.model import Subscribe
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
            sub = await get_subscription(session, user_id)

        data["subscription"] = sub
        data["has_subscription"] = sub is not None

        return await handler(event, data)