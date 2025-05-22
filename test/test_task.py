import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from app import models

client = TestClient(app)

@pytest.fixture(autouse=True, scope="module")
def setup_db():

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    proj = models.Project(name="Proj", description="")
    db.add(proj); db.commit(); db.refresh(proj)
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)

def test_create_task():
    response = client.post(
        "/tasks/",
        json={
            "title": "Task 1",
            "description": "Do something",
            "status": "pending",
            "project_id": 1
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Task 1"
    assert data["project_id"] == 1

def test_list_tasks():
    response = client.get("/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1

def test_get_task():
    response = client.get("/tasks/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1

def test_update_task():
    response = client.patch(
        "/tasks/1",
        json={"status": "done"}
    )
    assert response.status_code == 200
    assert response.json()["status"] == "done"

def test_delete_task():
    response = client.delete("/tasks/1")
    assert response.status_code == 204

    assert client.get("/tasks/1").status_code == 404

