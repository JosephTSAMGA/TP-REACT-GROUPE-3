from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    pseudo = Column(String(20), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    sessions = relationship(
        "GameSession", back_populates="user", cascade="all, delete-orphan"
    )
    badges = relationship(
        "UserBadge", back_populates="user", cascade="all, delete-orphan"
    )
    guesses = relationship("Guess", back_populates="user", cascade="all, delete-orphan")
