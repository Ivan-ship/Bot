from queries.model import User
from sqlalchemy import select

class GetAllUsers:
    def __init__(self, session):
        self.session = session
    
    async def get_all_user(self):
        result = await self.session.execute(select(User))
        return result.scalars().all()