from starlette.testclient import TestClient

from app.models.user import User


def test_get_all_users(client: TestClient, user_default: User):
    r = client.get("/v1/users")
    got = r.json()
    expected = [
        {
            "id": user_default.id,
            "email": user_default.email,
        }
    ]

    assert got == expected
