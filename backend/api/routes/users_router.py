import uuid

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db
from backend.schemas.user_schema import UserRead, UserUpdate
from backend.schemas.search_schema import SearchHistoryRead
from backend.services.user_service import (
    update_user_profile,
    get_user_history,
    delete_history_item,
    clear_user_history,
)

router = APIRouter(prefix="/api/v1/users", tags=["Users and History"])

@router.put("/profile")
def update_profile(
    user_id: uuid.UUID, payload: UserUpdate, db: Session = Depends(get_db)
) -> UserRead:
    return update_user_profile(db, user_id, payload)

@router.get("/history")
def get_history(user_id: uuid.UUID, db: Session = Depends(get_db)) -> list[SearchHistoryRead]:
    items = get_user_history(db, user_id)
    return [SearchHistoryRead.model_validate(x) for x in items]

@router.delete("/history/{id}")
def delete_history_item_route(
    id: uuid.UUID, user_id: uuid.UUID, db: Session = Depends(get_db)
):
    delete_history_item(db, user_id=user_id, history_id=id)
    return {"message": "History item deleted successfully"}

@router.delete("/history")
def clear_all_history(user_id: uuid.UUID, db: Session = Depends(get_db)):
    deleted = clear_user_history(db, user_id)
    return {"message": "All search history cleared", "deleted": deleted}