from aioredis.client import Redis
from fastapi import APIRouter, Depends, Request
from fastapi.exceptions import HTTPException
from starlette.responses import RedirectResponse

from app.dependencies.db import get_redis
from app.services.nonce_service import NonceService
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
async def redirect_app(req: Request, redis: Redis = Depends(get_redis)):
    shop_name = req.query_params.get("shop")
    if not shop_name:
        raise HTTPException(
            status_code=400, detail="Shop must be included in parameters"
        )
    is_valid = Verification().verify_hmac(req.query_params)
    if not is_valid:
        raise HTTPException(status_code=403, detail="Not allowed")
    nonce = req.query_params.get("state")
    if not nonce:
        raise HTTPException(status_code=400, detail="Invalid parameters")
    nonce_valid = await NonceService(redis).validate(shop_name, nonce)
    if not nonce_valid:
        raise HTTPException(status_code=403, detail="Invalid nonce")
    return {"message": "hi there"}
