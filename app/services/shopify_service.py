import httpx


class Shopify:
    async def get_permanent_token(self, shop_name: str) -> str:
        """Gets a permanent access token for a store"""
        url = f"https://{shop_name}/admin/oauth/access_token"
        # async with httpx
