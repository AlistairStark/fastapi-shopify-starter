from starlette.testclient import TestClient


def test_ping(client: TestClient):
    r = client.get("/v1/ping")

    got = r.json()
    expected = {"message": "pong"}

    assert r.status_code == 200
    assert got == expected
