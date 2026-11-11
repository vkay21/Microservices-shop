import os

# Use a throwaway SQLite database for tests (set before the app is imported).
os.environ["DATABASE_URL"] = "sqlite:///./test_users.db"

import pytest
from fastapi.testclient import TestClient

from app.db import Base, engine
from app.main import app


@pytest.fixture()
def client():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)


def register(client, email="ana@example.com"):
    return client.post(
        "/users/register",
        json={"email": email, "full_name": "Ana Lee", "password": "secret123"},
    )


def test_health(client):
    assert client.get("/health").json()["status"] == "ok"


def test_register_and_duplicate(client):
    r = register(client)
    assert r.status_code == 201
    assert "password" not in r.json() and "password_hash" not in r.json()
    assert register(client).status_code == 409


def test_login_and_me(client):
    register(client)
    r = client.post("/users/login", json={"email": "ana@example.com", "password": "secret123"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    me = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["email"] == "ana@example.com"


def test_wrong_password(client):
    register(client)
    r = client.post("/users/login", json={"email": "ana@example.com", "password": "nope123"})
    assert r.status_code == 401


def test_bad_token(client):
    r = client.get("/users/me", headers={"Authorization": "Bearer not-a-token"})
    assert r.status_code == 401


def test_get_user_by_id(client):
    user_id = register(client).json()["id"]
    assert client.get(f"/users/{user_id}").status_code == 200
    assert client.get("/users/9999").status_code == 404


def test_metrics_exposed(client):
    assert client.get("/metrics").status_code == 200
