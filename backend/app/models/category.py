from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), unique=True, nullable=False)
    slug = Column(String(80), unique=True, nullable=False)

    locations = relationship("Location", back_populates="category")
    sessions = relationship("GameSession", back_populates="category")
