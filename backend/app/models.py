"""Category (thème) et Location (lieu à deviner).

Une location appartient à une catégorie.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Category(Base):
    """Thème d'une partie : monuments, capitales, sites naturels..."""

    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    # Identifiant lisible et stable dans les URL et les filtres.
    slug: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)

    locations: Mapped[list["Location"]] = relationship(back_populates="category")


class Location(Base):
    """Lieu à deviner. Il appartient toujours à exactement une Category."""

    __tablename__ = "locations"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    # La réponse de la manche. Le score est calculé côté navigateur.
    latitude: Mapped[float] = mapped_column(Float, nullable=False)
    longitude: Mapped[float] = mapped_column(Float, nullable=False)
    image_url: Mapped[str] = mapped_column(Text, nullable=False)
    # Clé étrangère : pas de lieu orphelin, sans catégorie.
    category_id: Mapped[int] = mapped_column(
        ForeignKey("categories.id"),
        nullable=False,
        index=True,
    )

    category: Mapped["Category"] = relationship(back_populates="locations")


class GameSession(Base):
    """Partie démarrée : 5 lieux tirés au hasard (ou un autre effectif demandé)."""

    __tablename__ = "game_sessions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    # Nombre de lieux demandés (5 pour une partie normale).
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    # Null = tirage dans tous les thèmes. SET NULL si le thème est supprimé.
    category_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categories.id", ondelete="SET NULL"),
        nullable=True,
    )

    entries: Mapped[list["GameSessionLocation"]] = relationship(
        back_populates="session",
        order_by="GameSessionLocation.position",
        cascade="all, delete-orphan",
    )


class GameSessionLocation(Base):
    """Lien partie ↔ lieu, avec l'ordre du tirage (position 0, 1, 2...)."""

    __tablename__ = "game_session_locations"

    session_id: Mapped[str] = mapped_column(
        ForeignKey("game_sessions.id", ondelete="CASCADE"),
        primary_key=True,
    )
    location_id: Mapped[int] = mapped_column(
        ForeignKey("locations.id", ondelete="CASCADE"),
        primary_key=True,
    )
    position: Mapped[int] = mapped_column(Integer, nullable=False)

    session: Mapped["GameSession"] = relationship(back_populates="entries")
    location: Mapped["Location"] = relationship()
