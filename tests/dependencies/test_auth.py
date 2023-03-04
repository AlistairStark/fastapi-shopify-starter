import pytest

from app.dependencies.auth import authenticate_payload_and_signature


@pytest.mark.freeze_time("2022-01-29T00:13:57Z")
def test_authenticate_payload_and_signature_valid():
    jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJodHRwczovL2ludGVncmF0aW9uLXRlc3Qtc3RvcmUtYXRpay5teXNob3BpZnkuY29tL2FkbWluIiwiZGVzdCI6Imh0dHBzOi8vaW50ZWdyYXRpb24tdGVzdC1zdG9yZS5teXNob3BpZnkuY29tIiwiYXVkIjoiY2M3YjQyZWYyMGNjNWE3YTI1Y2I0Y2YzNDViOWNkN2MiLCJzdWIiOiI4MDE0NzY0NDY1OCIsImV4cCI6MTY0MzQxNTI1MywibmJmIjoxNjQzNDE1MTkzLCJpYXQiOjE2NDM0MTUxOTMsImp0aSI6ImE0OTEyYTI4LTc1NTgtNDI4ZC04ZWM3LTQ5NTM3NzRmMGMyNCIsInNpZCI6ImFiYmNkNjZhZWQxOTNkMDc1NGE0ZWJmOTYzNjk1MzQ5MGFhZWJhYTBjYWZhZGNmYmUyMGZkNDNjNTA5NjEwNTIifQ.WQFyn_G_4A-nqQUM5yLUxL_LyOsC1Su_XyrDjFI_jzo"
    got = authenticate_payload_and_signature(jwt)
    expected = {
        "aud": "cc7b42ef20cc5a7a25cb4cf345b9cd7c",
        "dest": "https://integration-test-store.myshopify.com",
        "exp": 1643415253,
        "iat": 1643415193,
        "iss": "https://integration-test-store.myshopify.com/admin",
        "jti": "a4912a28-7558-428d-8ec7-4953774f0c24",
        "nbf": 1643415193,
        "sid": "abbcd66aed193d0754a4ebf9636953490aaebaa0cafadcfbe20fd43c50961052",
        "sub": "80147644658",
    }
    assert got == expected
