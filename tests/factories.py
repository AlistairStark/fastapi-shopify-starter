import factory

from app import models
from app.models.database import SessionLocal


class BaseMeta:
    sqlalchemy_session = SessionLocal
    sqlalchemy_session_persistence = "commit"


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta(BaseMeta):
        model = models.User
