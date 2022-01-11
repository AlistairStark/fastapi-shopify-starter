from aioredis.client import Redis
from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.responses import RedirectResponse

from app.dependencies.db import get_redis, get_db
from app.services.nonce_service import NonceService
from app.services.shop_service import ShopService
from app.services.shopify_token_service import ShopifyToken
from app.services.verification import Verification

router = APIRouter()


@router.get("/install")
async def install_app(req: Request, redis: Redis = Depends(get_redis)):
    shop_name = req.query_params.get("shop")
    if not shop_name:
        raise HTTPException(
            status_code=400, detail="Shop must be included in parameters"
        )
    verification_service = Verification()
    is_valid = verification_service.verify_hmac(req.query_params)
    if not is_valid:
        raise HTTPException(status_code=403, detail="Not allowed")
    nonce_service = NonceService(redis)
    nonce = await nonce_service.create(shop_name)
    redirect_uri = verification_service.generate_redirect_url(nonce, shop_name)
    return RedirectResponse(url=redirect_uri)


@router.get("/redirect")
async def redirect_app(
    req: Request,
    redis: Redis = Depends(get_redis),
    db_session: AsyncSession = Depends(get_db),
):
    shop_url = req.query_params.get("shop")
    if not shop_url:
        raise HTTPException(
            status_code=400, detail="Shop must be included in parameters"
        )
    auth_code = req.query_params.get("code")
    if not auth_code:
        raise HTTPException(status_code=400, detail="Code parameter must be included")
    verification_service = Verification()
    shop_name = verification_service.validate_shop_name(shop_url)
    if not shop_name:
        raise HTTPException(status_code=400, detail="Shop name is required")
    is_valid = Verification().verify_hmac(req.query_params)
    if not is_valid:
        raise HTTPException(status_code=403, detail="Not allowed")
    nonce = req.query_params.get("state")
    if not nonce:
        raise HTTPException(status_code=400, detail="Invalid parameters")
    nonce_valid = await NonceService(redis).validate(shop_url, nonce)
    if not nonce_valid:
        raise HTTPException(status_code=403, detail="Invalid nonce")
    shop_service = ShopService(db_session, verification_service)
    shop = await shop_service.get_shop(shop_name)
    if not shop:
        token_response = await ShopifyToken().get_permanent_token(shop_url, auth_code)
        await ShopService(db_session, verification_service).create_shop(
            shop_name, token_response.access_token, token_response.scope
        )
    return f"<h1>TITLE {shop_name}</h1>"
