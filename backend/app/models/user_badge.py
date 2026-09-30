# =============================================================
# Table de liaison : UserBadge (un joueur débloque un badge)
# Relation N-N entre User et Badge, portée par cette table intermédiaire.
# =============================================================
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class UserBadge(Base):
    __tablename__ = "user_badges"
    # Un même joueur ne peut débloquer un même badge qu'une seule fois.
    __table_args__ = (UniqueConstraint("user_id", "badge_id", name="uq_user_badge"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    badge_id = Column(Integer, ForeignKey("badges.id"), nullable=False, index=True)
    unlocked_at = Column(DateTime(timezone=True), server_default=func.now())
    # Nom de lieu lisible ("Paris, France"), résolu par géolocalisation
    # inversée (Nominatim) au moment du déblocage. Null pour les badges
    # qui ne dépendent pas d'une position (ex: nombre de parties jouées).
    unlocked_place = Column(String(255), nullable=True)

    user = relationship("User", back_populates="badges")
    badge = relationship("Badge", back_populates="unlocks")
