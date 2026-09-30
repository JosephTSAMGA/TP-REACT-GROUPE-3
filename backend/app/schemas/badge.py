# =============================================================
# Schemas Pydantic pour Badge et UserBadge.
# =============================================================
from datetime import datetime

from pydantic import BaseModel, Field


class BadgeOut(BaseModel):
    id: int
    code: str
    name: str
    description: str

    model_config = {"from_attributes": True}


class BadgeEvaluateRequest(BaseModel):
    """Dernière position devinée par le joueur, envoyée par le frontend
    après une manche — sert uniquement au badge Explorateur international.
    Sans coordonnées, seuls les badges liés aux parties/au score sont
    évalués."""

    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)


class UserBadgeOut(BaseModel):
    id: int
    badge: BadgeOut
    unlocked_at: datetime
    unlocked_place: str | None = None

    model_config = {"from_attributes": True}
