from aiogram import BaseMiddleware
from repositories.create_user import CreateUser



class UserRegister(BaseMiddleware):
    async def __call__(self, handler, event, data):

        if event.from_user.username is None:
            await event.answer("Для использования бота необходимо добавить username в настройках Telegram.")
            return

        session = data["session"]
        repo = CreateUser(session)
        user = await repo.create_user(event.from_user)
        data["user"] = user
        return await handler(event, data)