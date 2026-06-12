from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from queries.config import settings
from sqlalchemy import text
import asyncio

async_engine = create_async_engine(
    url = settings.DATABASE_URL_asyncpg,
    echo = True,
    pool_size = 5,
    max_overflow = 10
)

SessionLocal = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_ = AsyncSession,
    autoflush=False
)

async def connection():
    async with async_engine.connect() as conn:
        res = await conn.execute(text("SELECT VERSION()"))
        version = res.scalar()
        print(version)
