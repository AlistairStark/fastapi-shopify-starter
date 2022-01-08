from aioredis.client import Redis
from sqlalchemy.ext.asyncio.session import AsyncSession


class DBService:
    def __init__(self, session: AsyncSession):
        self.session: AsyncSession = session


class RedisService:
    def __init__(self, redis: Redis):
        self.redis = redis
