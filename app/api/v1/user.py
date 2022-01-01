from __future__ import annotations

from typing import List
from fastapi import APIRouter
from app.services.user_service import UserService
from app.models.user import User

from pydantic import BaseModel

router = APIRouter()


class UserModel(BaseModel):
    id: int
    email: str


class UserModelList(BaseModel):
    users: List[UserModel]


@router.get("/users")
def get_all_users() -> UserModelList:
    users = UserService().get_all()
    user_list: UserModelList = {
        "users": [{"id": u.id, "email": u.email} for u in users]
    }
    return user_list
