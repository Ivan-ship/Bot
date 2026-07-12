from sqlalchemy import select, func, text
from queries.model import User, Subscribe

class AdminRepositories:
    def __init__(self, session):
        self.session = session
    
    async def get_users_count(self) -> int:
        return await self.session.scalar(
            select(func.count()).select_from(User)
        )
    
    async def get_today_users_count(self) -> int:
        return await self.session.scalar(
            select(func.count()).select_from(User).
            where(
                User.created_at >= func.current_date(),
                User.created_at < func.current_date() + text("INTERVAL '1 day'")
            )
        )
    
    async def get_vless_url_count(self) -> int:
        return await self.session.scalar(
            select(func.count()).select_from(Subscribe)
        )
    
    async def get_active_vless_url(self) -> int:
        return await self.session.scalar(
            select(func.count()).select_from(Subscribe).
            where(
                Subscribe.start_date <= func.current_date(),
                Subscribe.end_date >= func.current_date()
            )
        )
    
    async def get_disacrive_vless_url(self) -> int:
        return await self.session.scalar(
        select(func.count()).select_from(Subscribe).
        where(
            Subscribe.end_date <= func.current_date()
            )
        )


    async def get_statistics(self):
        return{
            "user_count": await self.get_users_count(),
            "today_user_count": await self.get_today_users_count(),
            "vless_url_count": await self.get_vless_url_count(),
            "active_vless_url": await self.get_active_vless_url(),
            "disacrive_vless_url": await self.get_disacrive_vless_url()
        }