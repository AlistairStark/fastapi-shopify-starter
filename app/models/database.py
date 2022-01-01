from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

from app.settings import DB_URL

engine = create_engine(DB_URL)

SessionLocal = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)


class DeclarativeBase:
    query = SessionLocal.query_property()


Base = declarative_base(cls=DeclarativeBase)
