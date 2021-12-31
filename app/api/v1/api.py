from fastapi import APIRouter
from app.api.v1.ping import router as ping_router

v1_router = APIRouter()

v1_router.include_router(ping_router, tags=["ping"])
