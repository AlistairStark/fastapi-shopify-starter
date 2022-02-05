import pytest

from app.dependencies.auth import authenticate_payload_and_signature, validate_webhook


@pytest.mark.freeze_time("2022-01-29T00:13:57Z")
def test_authenticate_payload_and_signature_valid():
    jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczpcL1wvaW50ZWdyYXRpb24tdGVzdC1zdG9yZS1hdGlrLm15c2hvcGlmeS5jb21cL2FkbWluIiwiZGVzdCI6Imh0dHBzOlwvXC9pbnRlZ3JhdGlvbi10ZXN0LXN0b3JlLWF0aWsubXlzaG9waWZ5LmNvbSIsImF1ZCI6ImJiN2M0MmVmMjBjYzVhN2EyNWNiNGNmMzQ1YjljZDdiIiwic3ViIjoiODAxNDc2NDQ2NTgiLCJleHAiOjE2NDM0MTUyNTMsIm5iZiI6MTY0MzQxNTE5MywiaWF0IjoxNjQzNDE1MTkzLCJqdGkiOiJhNDkxMmEyOC03NTU4LTQyOGQtOGVjNy00OTUzNzc0ZjBkMjQiLCJzaWQiOiJhYWFjZDY2YWVkMTkzZDA3NTRhNGViZjk2MzY5NTM0OTBhYWViYWEwY2FmYWRjZmJlMjBmZDQzYzUwOTYxMDUyIn0.qhQinxiY_zx7lh7DQ1jr0VFxtquxMMlWZTifqpA2Ric"
    got = authenticate_payload_and_signature(jwt)
    expected = {
        "aud": "bb7c42ef20cc5a7a25cb4cf345b9cd7b",
        "dest": "https://integration-test-store-atik.myshopify.com",
        "exp": 1643415253,
        "iat": 1643415193,
        "iss": "https://integration-test-store-atik.myshopify.com/admin",
        "jti": "a4912a28-7558-428d-8ec7-4953774f0d24",
        "nbf": 1643415193,
        "sid": "aaacd66aed193d0754a4ebf9636953490aaebaa0cafadcfbe20fd43c50961052",
        "sub": "80147644658",
    }
    assert got == expected


@pytest.mark.parametrize(
    ("header_hmac,body,expected"),
    [
        (
            "zT+ihbQU5psymo+keg7ytoKSdJCb0xmEr2ozcFYp4Zc=",
            b'{"shop_id":62122328306,"shop_domain":"integration-test-store-atik.myshopify.com","customer":{"id":6068768080114,"email":"allystark1000@gmail.com","phone":"+18199184407"},"orders_requested":[]}',
            True,
        ),
        (
            "zT+ihbQU5psymo+keg7ytoKSdJCb0xmEr2ozcFYp4Zc=",
            b'{"shop_id":1,"shop_domain":"integration-test-store-atik.myshopify.com","customer":{"id":6068768080114,"email":"allystark1000@gmail.com","phone":"+18199184407"},"orders_requested":[]}',
            False,
        ),
        (
            "aT+ihbQU5psymo+keg7ytoKSdJCb0xmEr2ozcFYp4Zc=",
            b'{"shop_id":62122328306,"shop_domain":"integration-test-store-atik.myshopify.com","customer":{"id":6068768080114,"email":"allystark1000@gmail.com","phone":"+18199184407"},"orders_requested":[]}',
            False,
        ),
    ],
)
def test_authenticate_shopify_webhook(header_hmac, body, expected):
    got = validate_webhook(header_hmac, body)
    assert got == expected
