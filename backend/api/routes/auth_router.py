from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from schemas.user_schema import UserCreate, UserLogin, UserRead
from services.user_service import register_user, login_user

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

@router.post("/register")
def register(payload: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    return register_user(db, payload)

@router.post("/login")
def login(payload: UserLogin, db: Session = Depends(get_db)) -> UserRead:
    return login_user(db, payload)