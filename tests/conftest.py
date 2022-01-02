from typing import final

import pytest
from fastapi.testclient import TestClient

from app import app
from app.models.database import Base, engine, get_session

# @pytest.fixture(autouse=True)
# def test_db():
#     # session = get_session()
#     # # try:
#     # Base.metadata.create_all(bind=engine)
#     yield
# except:
#     session.rollback()
# finally:
# Base.metadata.drop_all(bind=engine)
# session.commit()
# session.close()


@pytest.fixture
def client():
    test_client = TestClient(app)
    yield test_client
