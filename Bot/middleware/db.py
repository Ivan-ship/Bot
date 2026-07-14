from aiogram import BaseMiddleware
from queries.database import SessionLocal

class DbMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        async with SessionLocal() as session:
            data["session"] = session
            return await handler(event, data)