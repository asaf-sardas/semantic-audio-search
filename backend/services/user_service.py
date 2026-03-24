import uuid

import bcrypt
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.models.user import User
from backend.models.search_history import SearchHistory
from backend.schemas.user_schema import UserCreate, UserLogin, UserRead, UserUpdate


def _hash_password(password: str) -> str:
    hashed_bytes = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    return hashed_bytes.decode("utf-8")


def _verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))


def register_user(db: Session, data: UserCreate) -> UserRead:
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = User(
        email=data.email,
        password_hash=_hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return UserRead.model_validate(user)


def login_user(db: Session, data: UserLogin) -> UserRead:
    user = db.query(User).filter(User.email == data.email).first()
    if not user or not _verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )
    return UserRead.model_validate(user)


def update_user_profile(db: Session, user_id: uuid.UUID, data: UserUpdate) -> UserRead:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if data.email is not None:
        user.email = data.email
    if data.password is not None:
        user.password_hash = _hash_password(data.password)

    db.commit()
    db.refresh(user)
    return UserRead.model_validate(user)


def get_user_history(db: Session, user_id: uuid.UUID) -> list[SearchHistory]:
    return (
        db.query(SearchHistory)
        .filter(SearchHistory.user_id == user_id)
        .order_by(SearchHistory.searched_at.desc())
        .all()
    )


def delete_history_item(db: Session, user_id: uuid.UUID, history_id: uuid.UUID) -> None:

    item = (
        db.query(SearchHistory)
        .filter(SearchHistory.id == history_id, SearchHistory.user_id == user_id)
        .first()
    )
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="History item not found")

    db.delete(item)
    db.commit()


def clear_user_history(db: Session, user_id: uuid.UUID) -> int:
    deleted = db.query(SearchHistory).filter(SearchHistory.user_id == user_id).delete()
    db.commit()
    return deleted
