from queries.model import User
from sqlalchemy import select

class UserRepo:
    def __init__(self, session):
        self.session = session
    
    async def get_by_telegram_id(self, telegram_id: int):
        stmp = select(User).where(
            User.id == telegram_id
        )
        result = await self.session.execute(stmp)
        return result.scalar_one_or_none()