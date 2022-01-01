from __future__ import annotations
from typing import List

from app.models.user import User


class UserService:
    def get_all(self) -> List[User]:
        return User.query.all()
