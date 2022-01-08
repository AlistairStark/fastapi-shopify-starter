import pytest
from fastapi.exceptions import HTTPException

from app import settings
from app.services.verification import Verification


def test_verify_hmac():
    params = {
        "hmac": "d2eeb98093e30935fca5a721edd91f00e4a07f591e26ee0a91701b6f9efa99a7",
        "shop": "integration-test-store-atik.myshopify.com",
        "timestamp": "1641168465",
    }
    got = Verification().verify_hmac(params)
    expected = True

    assert got == expected


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
        ("https://example-shop.myshopify.com/", "example-shop"),
        ("https://invalid-shop.myshopify.com", None),
        ("", None),
        ("somerandomstring", None),
    ],
)
def test_validate_shop_name(shop_name, expected):
    got = Verification().validate_shop_name(shop_name)
    assert got == expected
