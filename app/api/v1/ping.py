import logging

from fastapi import APIRouter, Depends

from app.dependencies.auth import authenticate_shopify_jwt
from app.worker import tasks

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/ping")
async def ping_test(auth=Depends(authenticate_shopify_jwt)):
    return {"message": "pong"}


@router.post("/ping")
async def ping_test():
    return {"message": "post pong"}


@router.get("/ping-worker")
def ping_worker_test():
    tasks.test_task.delay("ping")
    return {"message": "celery pong"}
