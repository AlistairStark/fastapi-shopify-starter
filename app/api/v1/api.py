from fastapi import APIRouter

from app.api.v1.ping import router as ping_router
from app.api.v1.user import router as user_router
from app.api.v1.install import router as install_router

v1_router = APIRouter()

v1_router.include_router(ping_router, tags=["ping"])
v1_router.include_router(user_router, tags=["user"])
v1_router.include_router(install_router, tags=["install"])
