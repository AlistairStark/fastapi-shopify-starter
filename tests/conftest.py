import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker

from app import app
from app.models.database import Base
from app.settings import POSTGRES_USER, POSTGRES_PASSWORD, PROJECT_NAME

TEST_DB_NAME = "test"
TEST_DB_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{PROJECT_NAME}-postgres/{TEST_DB_NAME}"

engine = create_engine(TEST_DB_URL)

TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    test_client = TestClient(app)
    yield test_client
