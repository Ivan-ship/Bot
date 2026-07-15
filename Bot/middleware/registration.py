from aiogram import BaseMiddleware
from repositories.create_user import CreateUser



class UserRegister(BaseMiddleware):
    async def __call__(self, handler, event, data):
            session = data["session"]
            repo = CreateUser(session)
            user = await repo.create_user(event.from_user)
            data["user"] = user
            return await handler(event, data)