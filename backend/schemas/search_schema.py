from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=3)


class SearchResponse(BaseModel):
    query: str
    results: dict[str, Any] | list[Any] | None = None


class SearchHistoryBase(BaseModel):
    user_id: uuid.UUID
    content_id: str = Field(..., min_length=1, max_length=255)
    search_query: str = Field(..., min_length=1)
    results: dict[str, Any] | list[Any] | None = None


class SearchHistoryCreate(SearchHistoryBase):
    pass


class SearchHistoryRead(SearchHistoryBase):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    searched_at: datetime

