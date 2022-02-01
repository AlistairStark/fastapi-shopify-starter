import pytest
from starlette.testclient import TestClient

from tests.helpers import create_shop


@pytest.mark.asyncio
async def test_check_plan(client: TestClient, override_auth, db_session):
    await create_shop(
        {
            "shop_name": "test",
            "token": "12345",
            "scopes": "test1,test2",
            "dev_store": True,
            "subscribed": False,
        },
        db_session,
    )
    r = await client.get("/v1/check-plan")

    got = r.json()
    expected = {"valid": True}

    assert r.status_code == 200
    assert got == expected
