import secrets
from typing import Optional

from app.services.base import RedisService


class NonceService(RedisService):
    async def create(self, shop_name: str) -> bool:
        nonce = secrets.token_urlsafe()
        await self.redis.set(shop_name, nonce)
        return nonce

    async def get(self, shop_name: str) -> Optional[str]:
        val = await self.redis.get(shop_name)
        if val:
            return val.decode("utf-8")

    async def validate(self, shop_name: str, nonce: str) -> bool:
        saved_nonce = await self.get(shop_name)
        return saved_nonce == nonce

    async def delete(self, shop_name: str):
        await self.redis.delete(shop_name)
