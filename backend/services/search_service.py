import uuid
from sqlalchemy.orm import Session
from schemas.search_schema import SearchRequest, SearchResponse, TimestampResult
from models.search_history import SearchHistory

def perform_search(db: Session, request: SearchRequest, user_id: uuid.UUID | None = None) -> SearchResponse:

    #TODO search in the vectorDB return the data according to schema
    mock_results = [
        TimestampResult(start_time=120.5, end_time=135.0, relevance_score=0.92),
        TimestampResult(start_time=305.0, end_time=315.5, relevance_score=0.85)
    ]

    search_id = None

    if user_id:
        new_history = SearchHistory(
            user_id=user_id,
            content_id=request.content_id,
            search_query=request.query,
            results=[result.model_dump() for result in mock_results] 
        )
        db.add(new_history)
        db.commit()
        db.refresh(new_history)
        search_id = new_history.id

    return SearchResponse(
        search_id=search_id,
        query=request.query,
        results=mock_results
    )