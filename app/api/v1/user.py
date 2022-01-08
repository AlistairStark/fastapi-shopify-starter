from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio.session import AsyncSession

from app.dependencies.db import get_db
from app.services.user_service import UserService

router = APIRouter()


class UserModel(BaseModel):
    id: int
    email: str


@router.get("/users", response_model=List[UserModel])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    users = await user_service.get_all()
    return [{"id": u.id, "email": u.email} for u in users]
