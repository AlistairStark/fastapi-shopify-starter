import hashlib
import hmac
import re
from typing import Optional

from fastapi import HTTPException

from app import settings


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
            settings.SHOPIFY_APP_SECRET.encode("utf-8"),
            query_param_bytes,
            hashlib.sha256,
        )
        return got_hmac.hexdigest() == shopify_hmac

    def validate_shop_name(self, shop_name: str) -> Optional[str]:
        """Tests the shop name to ensure it is a valid match and parses the shop name"""
        pattern = r"\A(https|http)\:\/\/[a-zA-Z0-9][a-zA-Z0-9\-]*\.myshopify\.com\/"
        regex = re.compile(pattern)
        if regex.match(shop_name):
            m = re.search(r":\/\/(.*?).myshopify", shop_name)
            return m.group(1)

    def generate_redirect_url(self, nonce, shop_name) -> str:
        return f"https://{shop_name}/admin/oauth/authorize?client_id={settings.SHOPIFY_APP_KEY}&scope={settings.SCOPES}&redirect_uri={settings.REDIRECT_URL}&state={nonce}"
