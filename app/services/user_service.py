from __future__ import annotations

from typing import List

from app.models.user import User
from app.services.base import DBService


class UserService(DBService):
    def get_all(self) -> List[User]:
        return User.query.all()
