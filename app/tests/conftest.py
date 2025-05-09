from fastapi.testclient import TestClient
import pytest
from sqlmodel import SQLModel, Session, create_engine
from app.database import get_session
from app.main import app


@pytest.fixture
def client():
    engine = create_engine(
        "postgresql://postgres:postgres@localhost:5435/restaurant_db_test")
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        def override_get_session():
            yield session
        app.dependency_overrides[get_session] = override_get_session
        yield TestClient(app)
        app.dependency_overrides.clear()
