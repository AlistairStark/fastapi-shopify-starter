from __future__ import annotations

from typing import List

from sqlalchemy.ext.asyncio.result import AsyncResult
from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.future import select

from app.models.user import User
from app.services.base import DBService


class UserService(DBService):
    async def get_all(self) -> List[User]:
        session: AsyncSession
        async with self.session as session:
            result: AsyncResult = await session.execute(select(User))
            return result.scalars().all()

    async def create_one(self, email) -> User:
        async with self.session as session:
            u = User(email=email)
            session.add(u)
            await session.commit()
