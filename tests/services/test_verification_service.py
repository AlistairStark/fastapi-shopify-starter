import pytest
from fastapi.exceptions import HTTPException

from app import settings
from app.services.verification import Verification


def test_verify_hmac_no_hmac():
    params = {
        "shop": "integration-test-store-atik.myshopify.com",
        "timestamp": "1641168465",
    }
    with pytest.raises(HTTPException) as e:
        Verification().verify_hmac(params)
        assert e == "no HMAC param provided"


def test_generate_redirect_url():
    nonce = "12345"
    shop_name = "testshop.myshopify.com"
    got = Verification().generate_redirect_url(nonce, shop_name)
    expected = f"https://{shop_name}/admin/oauth/authorize?client_id={settings.SHOPIFY_APP_KEY}&scope={settings.SCOPES}&redirect_uri={settings.REDIRECT_URL}&state={nonce}"
    assert got == expected


@pytest.mark.parametrize(
    ("shop_name", "expected"),
    [
        ("example-shop.myshopify.com", "example-shop"),
        ("https://invalid-shop.myshopify.ca", None),
        ("", None),
        ("somerandomstring", None),
    ],
)
def test_validate_shop_name(shop_name, expected):
    got = Verification().validate_shop_name(shop_name)
    assert got == expected


@pytest.mark.parametrize(
    "test_str",
    [
        "test",
        "test-with-hyphens",
    ],
)
def test_encryption(test_str):
    verification = Verification()
    encrypted = verification.encrypt(test_str)
    got = verification.decrypt(encrypted)
    assert got == test_str
