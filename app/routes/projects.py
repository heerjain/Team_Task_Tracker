from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app import models, schemas
from app.dependencies import get_db

router = APIRouter()

@router.post(
    "/",
    response_model=schemas.ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    project: schemas.ProjectCreate,
    db: Session = Depends(get_db),
):
    db_proj = models.Project(**project.model_dump())
    db.add(db_proj)
    db.commit()
    db.refresh(db_proj)
    return db_proj

@router.get(
    "/",
    response_model=list[schemas.ProjectResponse],
    status_code=status.HTTP_200_OK,
)
def list_projects(db: Session = Depends(get_db)):
    return db.query(models.Project).all()

@router.get(
    "/{project_id}",
    response_model=schemas.ProjectResponse,
    status_code=status.HTTP_200_OK,
)
def get_project(project_id: int, db: Session = Depends(get_db)):
    proj = db.get(models.Project, project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    return proj

@router.put(
    "/{project_id}",
    response_model=schemas.ProjectResponse,
    status_code=status.HTTP_200_OK,
)
def update_project(
    project_id: int,
    updates: schemas.ProjectCreate,
    db: Session = Depends(get_db),
):
    proj = db.get(models.Project, project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    for field, value in updates.model_dump().items():
        setattr(proj, field, value)
    db.commit()
    db.refresh(proj)
    return proj

@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project(project_id: int, db: Session = Depends(get_db)):
    proj = db.get(models.Project, project_id)
    if not proj:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(proj)
    db.commit()
    return

