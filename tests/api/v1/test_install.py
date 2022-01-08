import pytest
from starlette.testclient import TestClient


@pytest.mark.asyncio
async def test_install(client: TestClient):
    params = {
        "hmac": "d2eeb98093e30935fca5a721edd91f00e4a07f591e26ee0a91701b6f9efa99a7",
        "shop": "integration-test-store-atik.myshopify.com",
        "timestamp": "1641168465",
    }

    r = await client.get("/v1/install", params=params)

    got = r.status_code
    expected = 307

    assert got == expected
