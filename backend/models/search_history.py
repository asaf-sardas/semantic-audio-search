import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy.sql import func

from backend.models.base import Base


class SearchHistory(Base):
    __tablename__ = "search_history"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False,index=True)
    content_id: Mapped[str] = mapped_column(String(255), ForeignKey("content.id"), nullable=False)
    search_query: Mapped[str] = mapped_column(Text, nullable=False)
    results: Mapped[dict | list] = mapped_column(JSONB, nullable=True)  
    searched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(),index=True)
    user: Mapped["User"] = relationship("User", back_populates="search_history")
    content: Mapped["Content"] = relationship("Content", back_populates="search_history")
