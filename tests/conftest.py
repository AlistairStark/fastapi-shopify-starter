import asyncio
from typing import Callable

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.testclient import TestClient

from app.dependencies.auth import AuthDetails, authenticate_shopify_jwt
from app.models.base import Base
from app.session import async_session, engine


@pytest.yield_fixture(scope="session")
def event_loop(request):
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
async def db_session() -> AsyncSession:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
        async with async_session(bind=connection) as session:
            yield session
            await connection.run_sync(Base.metadata.drop_all)


@pytest.fixture()
def override_get_db(db_session: AsyncSession) -> Callable:
    async def _override_get_db():
        yield db_session

    return _override_get_db


@pytest.fixture()
def app(override_get_db: Callable) -> FastAPI:
    from app import app
    from app.dependencies.db import get_db

    app.dependency_overrides[get_db] = override_get_db
    return app


@pytest.fixture()
async def client(app: FastAPI):
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture()
def sync_client():
    test_client = TestClient(app)
    yield test_client


def _auth_override():
    return AuthDetails(
        shop_name="test",
        shopify_user_id=1,
    )


@pytest.fixture()
def override_auth(app):
    app.dependency_overrides[authenticate_shopify_jwt] = _auth_override
