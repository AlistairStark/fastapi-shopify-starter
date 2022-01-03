from fastapi.exceptions import HTTPException
import pytest
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
