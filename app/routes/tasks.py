from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from app import models, schemas
from app.dependencies import get_db, verify_api_key

router = APIRouter(
    dependencies=[Depends(verify_api_key)]  # Apply API key check to all routes here
)

@router.post(
    "/",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
):
    # Verify parent project exists
    if not db.get(models.Project, task.project_id):
        raise HTTPException(status_code=404, detail="Parent project not found")
    db_task = models.Task(**task.model_dump())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get(
    "/",
    response_model=list[schemas.TaskResponse],
    status_code=status.HTTP_200_OK,
)
def list_tasks(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=100),
    status: str | None = Query(None, pattern="^(pending|in_progress|done)$"),
    project_id: int | None = None
):
    query = db.query(models.Task)

    if status:
        query = query.filter(models.Task.status == status)
    if project_id:
        query = query.filter(models.Task.project_id == project_id)

    tasks = query.offset(skip).limit(limit).all()
    return tasks


@router.get(
    "/{task_id}",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_200_OK,
)
def get_task(task_id: int, db: Session = Depends(get_db)):
    tk = db.get(models.Task, task_id)
    if not tk:
        raise HTTPException(status_code=404, detail="Task not found")
    return tk


@router.patch(
    "/{task_id}",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_200_OK,
)
def update_task(
    task_id: int,
    updates: schemas.TaskUpdate,
    db: Session = Depends(get_db),
):
    tk = db.get(models.Task, task_id)
    if not tk:
        raise HTTPException(status_code=404, detail="Task not found")
    # Only update fields that were set
    for field, value in updates.model_dump(exclude_unset=True).items():
        setattr(tk, field, value)
    db.commit()
    db.refresh(tk)
    return tk


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(task_id: int, db: Session = Depends(get_db)):
    tk = db.get(models.Task, task_id)
    if not tk:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(tk)
    db.commit()
    return
