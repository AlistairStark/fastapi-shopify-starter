from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio.result import AsyncResult
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.models.shop import Shop
from app.services.base import DBService
from app.services.verification import Verification


class ShopService(DBService):
    def __init__(
        self,
        db_session: AsyncSession,
        verification_service: Verification = Verification(),
    ):
        super().__init__(db_session)
        self.verification_service = verification_service

    async def create_shop(self, shop_name: str, access_token: str, scopes: str):
        token = self.verification_service.encrypt(access_token)
        session: AsyncSession
        async with self.session as session:
            s = Shop(shop_name=shop_name, token=token, scopes=scopes)
            session.add(s)
            await session.commit()

    async def get_shop(self, shop_name: str) -> Optional[Shop]:
        session: AsyncSession
        async with self.session as session:
            stmt = select(Shop).where(Shop.shop_name == shop_name)
            result: AsyncResult = await session.execute(stmt)
            return result.scalar_one_or_none()
