import logging

from fastapi import APIRouter, Depends, HTTPException
from starlette.responses import RedirectResponse
from app.dependencies.db import get_db, get_redis
from app.services.nonce_service import NonceService
from app.services.shop_service import ShopService
from app.dependencies.auth import AuthDetails, authenticate_shopify_jwt
from app.services.shopify_api_service import ShopifyApi
from app.settings import BASE_URL

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/check-plan")
async def check_plan(
    auth: AuthDetails = Depends(authenticate_shopify_jwt),
    db_session=Depends(get_db),
    redis=Depends(get_redis),
):
    shop = await ShopService(db_session).get_shop(auth.shop_name)
    if not shop:
        raise HTTPException(404, detail="Shop not found!")
    if not shop.store_is_valid():
        nonce = await NonceService(redis).create(f"{shop.shop_name}-sub")
        subscription_url = await ShopifyApi(shop).create_subscription(nonce)
        # redirect to subscription
        return {"valid": False, "redirect": subscription_url}
    return {"valid": True}


@router.get("/sub")
async def subscription_redirect(
    shop_name: str,
    nonce: str,
    charge_id: int,
    db_session=Depends(get_db),
    redis=Depends(get_redis),
):
    valid_nonce = NonceService(redis).validate(f"{shop_name}-sub", nonce)
    if not valid_nonce:
        raise HTTPException(403, detail="request not verified")
    shop_service = ShopService(db_session)
    shop = await shop_service.get_shop(shop_name)
    charge_id_str = f"{charge_id}"
    shop = await shop_service.update_shop(shop, {"charge_id": charge_id_str})
    return RedirectResponse(url=f"{BASE_URL}?host={shop.host}")
