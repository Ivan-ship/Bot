from queries.model import Subscribe
from sqlalchemy import select

class KeyRepository:
    def __init__(self, session):
        self.session = session

    
    async def get_user_key(self, telegram_id: int):
        stmp = select(Subscribe).where(Subscribe.id == telegram_id)

        result = await self.session.execute(stmp)
        return result.scalar_one_or_none()