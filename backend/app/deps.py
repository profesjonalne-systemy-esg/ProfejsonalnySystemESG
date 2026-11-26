"""Wspólne zależności. Plik należy do Epiku 2 (US 2.2 podmieni get_current_user na JWT).

Pozostałe epiki tylko importują get_current_user i get_project.
"""

import os

from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Project, User

DEMO_EMAIL = "specjalista@demo.pl"


def demo_mode() -> bool:
    """Tryb deweloperski: bez logowania działamy jako użytkownik demo. Domyślnie wyłączony."""
    return os.getenv("AUTH_DEMO", "false").lower() == "true"


def get_current_user(db: Session = Depends(get_db)) -> User:
    user = db.scalar(select(User).where(User.email == DEMO_EMAIL)) if demo_mode() else None
    if user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Zaloguj się, aby kontynuować")
    return user


def can_see_project(user: User, project: Project) -> bool:
    return project.owner_id == user.id or user.role in ("manager", "admin")


def get_project(
    project_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> Project:
    """Projekt z adresu URL. Cudzy projekt wygląda tak samo jak nieistniejący (404)."""
    project = db.get(Project, project_id)
    if project is None or not can_see_project(user, project):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Projekt nie istnieje")
    return project


def get_editable_project(
    project: Project = Depends(get_project), user: User = Depends(get_current_user)
) -> Project:
    """Projekt, który wolno zmieniać: własny i nieprzekazany do weryfikacji."""
    if project.owner_id != user.id and user.role != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Nie możesz zmieniać tego projektu")
    if project.status in ("in_review", "approved"):
        raise HTTPException(status.HTTP_409_CONFLICT, "Projekt jest zablokowany do edycji")
    return project
