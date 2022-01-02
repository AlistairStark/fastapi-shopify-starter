from sqlalchemy import Column, Integer, String

from app.models.database import Base
from app.models.helpers import CreatedAtUpdatedAtMixin


class User(Base, CreatedAtUpdatedAtMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
