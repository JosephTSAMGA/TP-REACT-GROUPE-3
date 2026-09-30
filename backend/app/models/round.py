from sqlalchemy import Boolean, Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class Round(Base):
    __tablename__ = "rounds"
    __table_args__ = (UniqueConstraint("session_id", "position", name="uq_round_position"),)

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(
        Integer, ForeignKey("game_sessions.id", ondelete="CASCADE"), nullable=False, index=True
    )
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False)
    position = Column(Integer, nullable=False)
    guessed = Column(Boolean, default=False, nullable=False)

    session = relationship("GameSession", back_populates="rounds")
    location = relationship("Location", back_populates="rounds")
    guess = relationship(
        "Guess", back_populates="round", uselist=False, cascade="all, delete-orphan"
    )
