# tests/test_projects.py

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine, SessionLocal
from sqlalchemy.orm import Session

client = TestClient(app)

# Use a fresh database for testing
@pytest.fixture(autouse=True, scope="module")
def setup_db():
    # Recreate tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_project():
    response = client.post(
        "/projects/",
        json={"name": "Test Project", "description": "A sample project"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Project"
    assert "id" in data
    assert "created_at" in data

def test_list_projects_empty_then_one():
    # After creation above, list should return 1
    response = client.get("/projects/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1

def test_get_project_by_id():
    # Assuming ID 1 exists
    response = client.get("/projects/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Test Project"

def test_update_project():
    response = client.put(
        "/projects/1",
        json={"name": "Updated", "description": "Updated desc"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated"

def test_delete_project():
    response = client.delete("/projects/1")
    assert response.status_code == 204
    # Now fetching should yield 404
    response = client.get("/projects/1")
    assert response.status_code == 404
