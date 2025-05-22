# app/schemas.py
from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional

# ── Project Schemas ──────────────────────────────────────────────────────────
class ProjectBase(BaseModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    """Payload when creating a new project."""
    pass

class ProjectResponse(ProjectBase):
    """What we send back when returning project data."""
    id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }


# ── Task Schemas ─────────────────────────────────────────────────────────────
class TaskBase(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    status: str = Field(..., pattern="^(pending|in_progress|done)$")
    due_date: Optional[date] = None

class TaskCreate(TaskBase):
    """Payload when creating a new task."""
    project_id: int

class TaskUpdate(BaseModel):
    """Payload when partially updating a task."""
    title: Optional[str]
    description: Optional[str]
    status: Optional[str] = Field(None, pattern="^(pending|in_progress|done)$")
    due_date: Optional[date]

class TaskResponse(TaskBase):
    """What we send back when returning task data."""
    id: int
    project_id: int
    created_at: datetime

    model_config = {
        "from_attributes": True
    }
