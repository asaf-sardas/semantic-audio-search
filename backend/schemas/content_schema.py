from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field
from models.content import ContentStatus,SourceType



class ContentBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=512)
    url: str = Field(..., min_length=1, max_length=2048)
    thumbnail_url: str | None = Field(default=None, max_length=2048)
    source_type: SourceType


class ContentCreate(ContentBase):
    id: str = Field(..., min_length=1, max_length=255)


class ContentUpdate(BaseModel):
    title: str | None = Field(default=None, min_length=1, max_length=512)
    url: str | None = Field(default=None, min_length=1, max_length=2048)
    thumbnail_url: str | None = Field(default=None, max_length=2048)
    source_type: SourceType | None = None
    status: ContentStatus | None = None


class ContentRead(ContentBase):
    model_config = ConfigDict(from_attributes=True)

    id: str
    status: ContentStatus
    created_at: datetime
    last_searched_at: datetime | None = None


class ContentStatusRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    status: ContentStatus
    last_searched_at: datetime | None = None

