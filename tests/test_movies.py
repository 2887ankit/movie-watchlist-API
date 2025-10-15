import os

from fastapi.testclient import TestClient

from app.main import app

# Ensure a test DB is used
os.environ["DATABASE_URL"] = "sqlite:///./test.db"


def test_create_and_filter_movies():
    with TestClient(app) as client:
        r1 = client.post("/items", json={"title": "Interstellar", "year": 2014, "watched": False})
        assert r1.status_code == 201

        r2 = client.post("/items", json={"title": "Inception", "year": 2010, "watched": True})
        assert r2.status_code == 201

        all_items = client.get("/items")
        assert all_items.status_code == 200
        assert len(all_items.json()) >= 2

        only_unwatched = client.get("/items", params={"watched": "false"})
        assert only_unwatched.status_code == 200
        data = only_unwatched.json()
        assert any(m["title"] == "Interstellar" for m in data)