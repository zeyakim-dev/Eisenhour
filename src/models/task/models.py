from sqlalchemy import Boolean, Column, DateTime, Integer, String, func

from src.core.db import Base


class Task(Base):  # type: ignore
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    is_important = Column(Boolean, default=False)
    is_urgent = Column(Boolean, default=False)
    is_completed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)
    user_id = Column(Integer, index=True)  # Assuming a user model will be added later
