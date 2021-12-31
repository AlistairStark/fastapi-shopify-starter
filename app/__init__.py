__version__ = "0.1.0"

from fastapi import FastAPI

from app import settings
from app.api.v1.api import v1_router

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(v1_router, prefix="/v1")
