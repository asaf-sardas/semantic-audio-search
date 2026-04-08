import uuid
from datetime import datetime
from enum import Enum 
from sqlalchemy import String, DateTime, Enum as SQLEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column,relationship
from sqlalchemy.sql import func

from models.base import Base

class UserRole(str, Enum):
    USER = "user"         
    ADMIN = "admin"

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(SQLEnum(UserRole), default=UserRole.USER)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now())
    search_history: Mapped[list["SearchHistory"]] = relationship("SearchHistory", back_populates="user", cascade="all, delete-orphan")
