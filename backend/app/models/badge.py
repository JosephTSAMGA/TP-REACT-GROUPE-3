# =============================================================
# Ressource CRUD : Badge (récompense débloquable)
# Le catalogue est fixe et rempli au démarrage (voir app/seed_badges.py) —
# ce n'est pas une ressource que les joueurs créent eux-mêmes.
# =============================================================
from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship

from app.database import Base


class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True, index=True)
    # Identifiant stable utilisé dans le code (services/badges.py) pour
    # reconnaître un badge sans dépendre de son id numérique en base.
    code = Column(String(50), unique=True, nullable=False, index=True)
    name = Column(String(80), nullable=False)
    description = Column(Text, nullable=False)

    # Relation inverse : tous les déblocages de ce badge, tous joueurs confondus.
    unlocks = relationship(
        "UserBadge", back_populates="badge", cascade="all, delete-orphan"
    )
