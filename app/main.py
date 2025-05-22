from fastapi import FastAPI
from typing import Union

app = FastAPI(title="Team Task Tracker API")

# === /projects endpoints ===

@app.get("/projects/")
def get_projects():
    return {"message": "List of all projects"}

@app.post("/projects/")
def create_project(name: str, description: Union[str, None] = None):
    return {"message": "Project created", "name": name, "description": description}

# === /tasks endpoints ===

@app.get("/tasks/")
def get_tasks():
    return {"message": "List of all tasks"}

@app.post("/tasks/")
def create_task(title: str, status: str = "pending", project_id: int = 1):
    return {
        "message": "Task created",
        "title": title,
        "status": status,
        "project_id": project_id
    }

# app/main.
from fastapi import FastAPI
from app.routes import projects, tasks

app = FastAPI(title="Team Task Tracker API")

app.include_router(
    projects.router,
    prefix="/projects",
    tags=["Projects"]
)
app.include_router(
    tasks.router,
    prefix="/tasks",
    tags=["Tasks"]
)






