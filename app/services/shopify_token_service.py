from dataclasses import dataclass

import httpx
from httpx import Response

from app import settings


@dataclass
class TokenResponse:
    access_token: str
    scope: str


class ShopifyToken:
    async def get_permanent_token(self, shop_name: str, code: str) -> TokenResponse:
        """Gets a permanent access token for a store"""
        url = f"https://{shop_name}/admin/oauth/access_token"
        client: httpx.AsyncClient
        async with httpx.AsyncClient() as client:
            data = {
                "code": code,
                "client_id": settings.SHOPIFY_APP_KEY,
                "client_secret": settings.SHOPIFY_APP_SECRET,
            }
            try:
                r: Response = await client.post(url, data=data)
                r.raise_for_status()
                return TokenResponse(**r.json())
            except httpx.HTTPError as exc:
                print(f"HTTP Exception for {exc.request.url} - {exc}")
