from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from typing import List, Optional
from app import models, schemas
from app.dependencies import get_db, verify_api_key

router = APIRouter(
    prefix="/projects",
    tags=["Projects"],
    dependencies=[Depends(verify_api_key)]  # API key security on all routes here
)

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
    response_model=List[schemas.ProjectResponse],
    status_code=status.HTTP_200_OK,
)
def list_projects(
    db: Session = Depends(get_db),
    name: Optional[str] = Query(None, description="Search by project name"),
    created_after: Optional[date] = Query(None, description="Projects created after this date"),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(10, le=100, description="Max number of records to return"),
):
    query = db.query(models.Project)

    if name:
        query = query.filter(models.Project.name.ilike(f"%{name}%"))

    if created_after:
        query = query.filter(models.Project.created_at >= created_after)

    return query.offset(skip).limit(limit).all()


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



