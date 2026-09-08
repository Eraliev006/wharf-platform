from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.core.settings import settings

async_engine = create_async_engine(url=settings.db_url, pool_size=10, max_overflow=20)

async_session_maker = async_sessionmaker(
    bind=async_engine, expire_on_commit=False, autoflush=False
)


async def get_db() -> AsyncGenerator[AsyncSession]:
    async with async_session_maker() as session:
        yield session
