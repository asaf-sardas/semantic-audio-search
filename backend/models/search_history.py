# טבלה: search_history (היסטוריית חיפושים)
# user_id מצביע על users.id, content_id מצביע על content.id
import uuid
from datetime import datetime
from sqlalchemy import String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from models.base import Base


class SearchHistory(Base):
    __tablename__ = "search_history"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content_id: Mapped[str] = mapped_column(String(255), ForeignKey("content.id"), nullable=False)
    search_query: Mapped[str] = mapped_column(Text, nullable=False)
    results: Mapped[dict | list] = mapped_column(JSONB, nullable=True)  
    searched_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
