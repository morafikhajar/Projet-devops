import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from app import app, db


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.app_context():
        db.create_all()
    with app.test_client() as client:
        yield client


def test_home_page_loads(client):
    res = client.get("/")
    assert res.status_code == 200


def test_add_task(client):
    client.post("/add", data={"title": "buy bread", "tags": "Shopping", "date": "Nov 5", "status": "todo"})
    res = client.get("/")
    assert "buy bread".encode() in res.data


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"
