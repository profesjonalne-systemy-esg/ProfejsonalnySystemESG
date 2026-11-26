"""Epik 2: rejestracja, logowanie."""

from fastapi import APIRouter, Depends

from app.deps import get_current_user
from app.models import User
from app.schemas.user import UserOut

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.get("/me", response_model=UserOut)
def me(user: User = Depends(get_current_user)):
    return user
