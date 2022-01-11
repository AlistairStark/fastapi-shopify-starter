from sqlalchemy import Column, Integer, String

from app.models.base import Base
from app.models.helpers import CreatedAtUpdatedAtMixin


class Shop(Base, CreatedAtUpdatedAtMixin):
    __tablename__ = "shop"

    id = Column(Integer, primary_key=True, index=True)
    shop_name = Column(String, index=True, unique=True)
    token = Column(String)
    scopes = Column(String)
