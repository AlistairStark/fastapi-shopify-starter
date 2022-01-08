from aioredis.client import Redis
from sqlalchemy.ext.asyncio import AsyncSession

from app.redis import get_redis_session
from app.session import async_session


async def get_db() -> AsyncSession:
    """
    Dependency function that yields db sessions
    """
    async with async_session() as session:
        yield session
        await session.commit()


def get_redis() -> Redis:
    return get_redis_session()
