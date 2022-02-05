import logging
from typing import Optional
from fastapi import HTTPException
import httpx
from app.models.shop import Shop

from app.services.verification import Verification


logger = logging.getLogger(__name__)


class ShopifyRest:
    def __init__(
        self,
        shop: Shop,
        verification_service: Verification = Verification(),
    ) -> None:
        self.shop = shop
        self.verification_service = verification_service
        token = self.verification_service.decrypt(shop.token)
        headers = {
            "X-Shopify-Access-Token": token,
        }
        url = f"https://{shop.shop_name}.myshopify.com/admin/api/2022-01"
        self.client = httpx.AsyncClient(headers=headers, base_url=url)

    async def get(
        self,
        endpoint: str,
        params: Optional[dict] = {},
    ) -> dict:
        session: httpx.AsyncClient
        async with self.client as session:
            try:
                result = await session.get(endpoint, params=params)
                result.raise_for_status()
                return result.json()
            except httpx.HTTPStatusError as exc:
                logger.error(
                    f"Error response {exc.response.status_code} while requesting {exc.request.url!r}."
                )
                return {"error": True, "status_code": exc.response.status_code}
            except Exception as e:
                logger.error(e)
                raise HTTPException(
                    502, detail="There was an error communicating with Shopify"
                )

    async def check_subscription(self, charge_id: str) -> bool:
        res = await self.get(f"/recurring_application_charges/{charge_id}.json")
        if res.get("error") and res.get("status_code") == 404:
            return False
        charge_active = res.get("recurring_application_charge", {}).get("status")
        logger.info(
            f"Shop {self.shop.shop_name} has charge state {charge_active} - charge ID {charge_id}"
        )
        return charge_active and charge_active == "active"
