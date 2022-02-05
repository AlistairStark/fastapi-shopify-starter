import base64
import hashlib
import hmac
import json
import logging
from dataclasses import dataclass
from datetime import datetime
from typing import List

from fastapi import HTTPException, Request

from app import settings

logger = logging.getLogger(__name__)


def _decode_to_json(part: str) -> dict:
    return json.loads(base64.b64decode(part + "==").decode())


def _extract_property(d: dict, prop: str):
    try:
        return d[prop]
    except Exception as e:
        logger.error(f"Failed to extract {prop} from {d}. \n{e}")


def _test_urls_match(iss: str, dest: str) -> bool:
    SHOPIFY_DOMAIN = "myshopify.com"
    url_1 = iss.split(SHOPIFY_DOMAIN)[0]
    url_2 = dest.split(SHOPIFY_DOMAIN)[0]
    return url_1 == url_2


def _verify_signature(jwt_split: List[str]) -> bool:
    digest = hmac.new(
        settings.SHOPIFY_APP_SECRET.encode("utf-8"),
        msg=f"{jwt_split[0]}.{jwt_split[1]}".encode("utf-8"),
        digestmod=hashlib.sha256,
    ).digest()
    signature = (
        base64.b64encode(digest).decode("utf-8").replace("+", "-").replace("/", "_")
    )
    return signature == f"{jwt_split[2]}="


def authenticate_payload_and_signature(jwt: str) -> dict:
    try:
        jwt_split = jwt.split(".")
        payload = _decode_to_json(jwt_split[1])
        now = datetime.now()
        exp = _extract_property(payload, "exp")
        if datetime.fromtimestamp(exp) <= now:
            raise ValueError(f"Value exp {exp} is not in the future")
        nbf = _extract_property(payload, "nbf")
        if datetime.fromtimestamp(nbf) >= now:
            raise ValueError(f"Value nbf {nbf} is not in the past")
        iss = _extract_property(payload, "iss")
        dest = _extract_property(payload, "dest")
        if not _test_urls_match(iss, dest):
            raise ValueError(f"Value iss {iss} and dest {dest} don't match")
        aud = _extract_property(payload, "aud")
        if aud != settings.SHOPIFY_APP_KEY:
            raise ValueError(f"aud {aud} does not match public key")
        if not payload.get("sub"):
            raise ValueError("No sub value in payload")
        if not _verify_signature(jwt_split):
            raise ValueError("Token signature doesn't match")
        return payload
    except Exception as e:
        logger.error(e)
        raise HTTPException(401, detail="Invalid JWT")


def _get_shop_name(shop_url: str) -> str:
    try:
        remove_schema = shop_url.replace("https://", "")
        return remove_schema.split(".")[0]
    except Exception as e:
        logger.error(e)


@dataclass
class AuthDetails:
    shop_name: str
    shopify_user_id: str


def authenticate_shopify_jwt(request: Request) -> AuthDetails:
    shopify_jwt = request.headers.get("authorization")
    if not shopify_jwt:
        raise HTTPException(status_code=403, detail="Forbidden")
    payload = authenticate_payload_and_signature(shopify_jwt)
    shop_name = _get_shop_name(payload["dest"])
    return AuthDetails(shop_name=shop_name, shopify_user_id=payload["sub"])


def validate_webhook(header_hmac: str, data: bytes) -> bool:
    digest = hmac.new(
        settings.SHOPIFY_APP_SECRET_ENCODED, data, hashlib.sha256
    ).digest()
    computed_hmac = base64.b64encode(digest)
    return hmac.compare_digest(computed_hmac, header_hmac.encode("utf-8"))


async def authenticate_shopify_webhook(request: Request) -> bool:
    """Verifies the authenticity of a shopify webhook request"""
    shopify_hmac: str = request.headers.get("X-Shopify-Hmac-SHA256")
    data = await request.body()
    if not shopify_hmac:
        raise HTTPException(400, detail="Invalid headers")
    valid = validate_webhook(shopify_hmac, data)
    if not valid:
        raise HTTPException(403, detail="Forbidden")
    return valid
