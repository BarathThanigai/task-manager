import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

os.environ["SECRET_KEY"] = "test-secret-key"
os.environ["DATABASE_URL"] = "sqlite+pysqlite:///:memory:"

from app.db.session import Base, get_db
from app.main import app


@pytest.fixture
def client():
    test_engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session_local = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)
    test_engine.dispose()


@pytest.fixture
def auth_headers(client):
    registration_payload = {
        "username": "alice",
        "email": "alice@example.com",
        "password": "secret123",
    }
    client.post("/register", json=registration_payload)
    response = client.post("/login", json={"username": "alice", "password": "secret123"})
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
