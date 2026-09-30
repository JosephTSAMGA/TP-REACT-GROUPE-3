import os

os.environ["DATABASE_URL"] = "sqlite:///./test.db"
os.environ["JWT_SECRET_KEY"] = "test-secret-key"

import pytest
from fastapi.testclient import TestClient

from app.database import Base, SessionLocal, engine
from app.main import app
from app.seed import seed_all


@pytest.fixture(scope="function", autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_all(db)
    finally:
        db.close()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def auth_headers(client):
    client.post(
        "/api/auth/register",
        json={"pseudo": "Zouzou", "email": "zouzou@test.com", "password": "motdepasse123"},
    )
    response = client.post(
        "/api/auth/login", json={"email": "zouzou@test.com", "password": "motdepasse123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
