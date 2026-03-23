from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.schemas.search_schema import SearchRequest, SearchResponse
from backend.database import get_db

from backend.services import search_service

router = APIRouter(prefix="/api/v1/search", tags=["Search"])

@router.post("/", response_model=SearchResponse)
def search(request: SearchRequest, db: Session = Depends(get_db)):
    search_response= search_service.perform_search(db=db, request=request, user_id=None)
    return search_response