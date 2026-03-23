from __future__ import annotations

import uuid
from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class TimestampResult(BaseModel):
    start_time: float
    end_time: float
    relevance_score: float

class SearchRequest(BaseModel):
    query: str = Field(..., min_length=3)
    content_id: str = Field(..., min_length=1, max_length=255) 

class SearchResponse(BaseModel):
    id: uuid.UUID | None = None    
    query: str
    results: list[TimestampResult]

class SearchHistoryBase(BaseModel):
    user_id: uuid.UUID
    content_id: str = Field(..., min_length=1, max_length=255)
    search_query: str = Field(..., min_length=1)
    results: list[TimestampResult] 

class SearchHistoryCreate(SearchHistoryBase):
    pass

class SearchHistoryRead(SearchHistoryBase):
    model_config = ConfigDict(from_attributes=True)
    id: uuid.UUID
    searched_at: datetime