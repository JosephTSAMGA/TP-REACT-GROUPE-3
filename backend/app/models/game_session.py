from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class GameSession(Base):
    __tablename__ = "game_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    size = Column(Integer, default=5, nullable=False)
    score_total = Column(Integer, default=0, nullable=False)
    finished = Column(Boolean, default=False, nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    finished_at = Column(DateTime(timezone=True), nullable=True)

    user = relationship("User", back_populates="sessions")
    category = relationship("Category", back_populates="sessions")
    rounds = relationship(
        "Round",
        back_populates="session",
        cascade="all, delete-orphan",
        order_by="Round.position",
    )
