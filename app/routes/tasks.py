from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.dependencies import get_db

router = APIRouter()

@router.post(
    "/",
    response_model=schemas.TaskResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_task(
    task: schemas.TaskCreate,
    db: Session = Depends(get_db),
):
    # Verify the parent project exists
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
def list_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

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
    # Only update fields the client sent
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

