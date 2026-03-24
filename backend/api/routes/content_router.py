from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session


from backend.database import get_db
from backend.schemas.content_schema import ContentCreate,ContentRead,ContentStatusRead, ContentPreviewResponse
from backend.services.content_service import get_content_by_id,process_content,preview_content

router = APIRouter(prefix="/api/v1/content", tags=["Content"])

@router.get("/{id}/status", response_model=ContentStatusRead)
def get_status(id: str, db: Session = Depends(get_db)):
    content = get_content_by_id(db, id)
    return content

@router.get("/{id}", response_model=ContentRead)
def get_content(id: str, db: Session = Depends(get_db)):
    content = get_content_by_id(db, id)
    return content

@router.post("/preview", response_model=ContentPreviewResponse)
def preview(payload: ContentCreate):
    result = preview_content(payload)
    return result

@router.post("/process", response_model=ContentRead)
def process(payload: ContentCreate, db: Session = Depends(get_db)):
    result = process_content(db, payload)
    return result