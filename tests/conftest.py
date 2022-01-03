import pytest
from fastapi.testclient import TestClient

from app import app
from app.models.database import Base, engine, get_session
from tests import factories

Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


@pytest.fixture(autouse=True)
def test_db():
    tables = []
    for t in Base.metadata.sorted_tables:
        tables.append(f'"{t.name}"')
    stmt = f"TRUNCATE {','.join(tables)};"
    s = get_session()
    s.execute(stmt)
    s.commit()
    s.close_all()


@pytest.fixture
def client():
    test_client = TestClient(app)
    yield test_client


@pytest.fixture
def user_default():
    return factories.UserFactory(email="testmail@test.com")
