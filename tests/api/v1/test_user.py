import pytest
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.testclient import TestClient

from app.models.user import User
from app.services.user_service import UserService


async def make_user(email: str, db_session: AsyncSession):
    async with db_session as session:
        u = User(email=email)
        session.add(u)
        await session.commit()


@pytest.mark.asyncio
async def test_get_all_users(client: TestClient, db_session):
    u = await make_user("test", db_session)
    r = await client.get("/v1/users")
    got = r.json()
    expected = [
        {
            "id": 1,
            "email": "test",
        }
    ]

    assert got == expected
