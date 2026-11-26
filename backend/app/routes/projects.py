"""Epik 2: projekty raportowe. Baza daje tylko odczyt, resztę CRUD dodaje US 2.5."""

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user, get_project
from app.models import Project, User
from app.schemas.project import ProjectOut

router = APIRouter(prefix="/api/projects", tags=["projects"])


@router.get("", response_model=list[ProjectOut])
def list_projects(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    query = select(Project).order_by(Project.updated_at.desc(), Project.id.desc())
    if user.role == "specialist":
        query = query.where(Project.owner_id == user.id)
    return db.scalars(query).all()


@router.get("/{project_id}", response_model=ProjectOut)
def read_project(project: Project = Depends(get_project)):
    return project
