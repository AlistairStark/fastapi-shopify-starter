from sqlalchemy import Boolean, Column, Integer, String

from app.models.base import Base
from app.models.helpers import CreatedAtUpdatedAtMixin, make_timestamptz


class Shop(Base, CreatedAtUpdatedAtMixin):
    __tablename__ = "shop"

    id = Column(Integer, primary_key=True, index=True)
    shop_name = Column(
        String,
        index=True,
        unique=True,
        doc="Name of shop with https:// and myshopify.com removed",
    )
    token = Column(String, doc="hashed permanent access token")
    scopes = Column(String, doc="shopify API scopes")
    host = Column(String, doc="Shopify encoded host. Required for app bridge")
    dev_store = Column(Boolean, default=False)
    charge_id = Column(String, nullable=True)
    free_trial_end = Column(make_timestamptz(), nullable=True)

    def store_is_valid(self) -> bool:
        """Check if this store is valid"""
        return self.dev_store or self.charge_id
