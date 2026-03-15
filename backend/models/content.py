from datetime import datetime
from enum import Enum
from sqlalchemy import String, DateTime, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from models.base import Base


class SourceType(str, Enum):
    YOUTUBE = "youtube"
    PODCAST = "podcast"
    OTHER = "other"


class ContentStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    READY = "ready"
    FAILED = "failed"


class Content(Base):
    __tablename__ = "content"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)  
    title: Mapped[str] = mapped_column(String(512), nullable=False)
    url: Mapped[str] = mapped_column(String(2048), nullable=False)
    source_type: Mapped[SourceType] = mapped_column(SQLEnum(SourceType), 
    nullable=False)
    status: Mapped[ContentStatus] = mapped_column(SQLEnum(ContentStatus),
     default=ContentStatus.PENDING)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
     default=func.now())
    last_searched_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True),
     server_default=func.now(), onupdate=func.now())
