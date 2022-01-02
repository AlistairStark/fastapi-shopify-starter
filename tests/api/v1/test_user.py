from starlette.testclient import TestClient


def test_get_all_users(client: TestClient):
    r = client.get("/v1/users")
    print("r: ", r.json())
    assert False
