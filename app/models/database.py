from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.orm.session import Session

from app import settings


def make_engine():
    return create_engine(settings.get_db_url())


engine = make_engine()

SessionLocal = scoped_session(sessionmaker(bind=engine))


def get_session(*args, **kwargs) -> Session:
    return SessionLocal(*args, **kwargs)


class DeclarativeBase:
    query = SessionLocal.query_property()


Base = declarative_base(cls=DeclarativeBase)
