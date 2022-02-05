import logging
from typing import List

from fastapi import APIRouter, Depends
from app.dependencies.auth import authenticate_shopify_webhook
from pydantic import BaseModel

logger = logging.getLogger(__name__)

router = APIRouter()


class Customer(BaseModel):
    id: int
    email: str
    phone: str


class DataRequest(BaseModel):
    id: int


class CustomerDataRequest(BaseModel):
    shop_id: int
    shop_domain: str
    orders_requested: List[int]
    customer: Customer
    data_request: DataRequest


@router.post("/customer-data-request")
async def customer_data_request(
    body: CustomerDataRequest,
    auth=Depends(authenticate_shopify_webhook),
):
    logger.info(f"Customer data request: \n {body}")
    return {"message": "pong"}


class CustomerRedact(BaseModel):
    shop_id: int
    shop_domain: str
    customer: Customer
    orders_to_redact: List[int]


@router.post("/customer-data-erasure")
async def customer_data_request(
    body: CustomerRedact,
    auth=Depends(authenticate_shopify_webhook),
):
    logger.info(f"Customer data erasure \n {body}")
    return {"message": "pong"}


class ShopRedact(BaseModel):
    shop_id: int
    shop_domain: str


@router.post("/shop-data-erasure")
async def customer_data_request(
    body: ShopRedact,
    auth=Depends(authenticate_shopify_webhook),
):
    logger.info(f"Shop data erasure \n {body}")
    return {"message": "pong"}
