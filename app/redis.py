import aioredis
from aioredis.client import Redis

from app import settings

redis = aioredis.from_url(settings.REDIS_URI)


def get_redis_session() -> Redis:
    return redis
