from fastapi import APIRouter, Request
from fastapi.exceptions import HTTPException

from app.services.nonce_service import NonceService
from app.services.verification import Verification

router = APIRouter()


@router.get("/install")
async def install_app(req: Request):
    shop_name = req.query_params.get("shop")
    if not shop_name:
        raise HTTPException(
            status_code=400, detail="Shop must be included in parameters"
        )
    is_valid = Verification().verify_hmac(req.query_params)
    if not is_valid:
        raise HTTPException(status_code=403, detail="Not allowed")
    nonce_service = NonceService()
    nonce = await nonce_service.create(shop_name)
    return {"message": nonce}


@router.get("/redirect")
def redirect_app():
    return {"message": "hi there"}
