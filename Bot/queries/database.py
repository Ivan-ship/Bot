from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from queries.config import settings
from sqlalchemy import text
import asyncio
from queries.base import Base

async_engine = create_async_engine(
    url = settings.DATABASE_URL_asyncpg,
    echo = True,
    pool_size = 5,
    max_overflow = 10
)

async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

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
