import pytest
from starlette.testclient import TestClient


@pytest.mark.asyncio
async def test_ping(client: TestClient, override_auth):
    r = await client.get("/v1/ping")

    got = r.json()
    expected = {"message": "pong"}

    assert r.status_code == 200
    assert got == expected
