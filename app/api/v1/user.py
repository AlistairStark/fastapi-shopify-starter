from __future__ import annotations

from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from app.services.user_service import UserService

router = APIRouter()


class UserModel(BaseModel):
    id: int
    email: str


@router.get("/users", response_model=List[UserModel])
def get_all_users():
    users = UserService().get_all()
    return [{"id": u.id, "email": u.email} for u in users]
