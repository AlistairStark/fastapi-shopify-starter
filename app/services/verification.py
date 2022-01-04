import hashlib
import hmac

from fastapi import HTTPException

from app.settings import SHOPIFY_APP_SECRET


class Verification:
    def _make_message_bytestr(self, q_params: dict) -> bytes:
        sorted(q_params)
        return "&".join(
            [f"{key}={value}" for key, value in q_params.items() if key != "hmac"]
        ).encode("utf-8")

    def verify_hmac(self, query_params: dict) -> bool:
        """Verifies string through an HMAC-SHA256 hash function using the app secret key.
        Compares to the hmac shopify sends.
        """
        shopify_hmac = query_params.get("hmac")
        if not shopify_hmac:
            raise HTTPException(status_code=400, detail="no HMAC param provided")
        query_param_bytes = self._make_message_bytestr(query_params)
        got_hmac = hmac.new(
            SHOPIFY_APP_SECRET.encode("utf-8"),
            query_param_bytes,
            hashlib.sha256,
        )
        return got_hmac.hexdigest() == shopify_hmac

    def generate_redirect_url(self, nonce, shop_name) -> str:
        return ""
