from datetime import datetime

from pydantic import BaseModel, Field


class GameSessionUpdate(BaseModel):
    score_total: int | None = Field(default=None, ge=0)
    finished: bool | None = None


class RoundPlayOut(BaseModel):
    """Manche jouable : jamais de lat/lng ni du nom du lieu avant le guess."""

    id: int
    session_id: int
    position: int
    image_url: str
    guessed: bool

    model_config = {"from_attributes": True}


class GameSessionOut(BaseModel):
    id: int
    user_id: int
    category_id: int | None
    size: int
    score_total: int
    finished: bool
    started_at: datetime
    finished_at: datetime | None
    rounds: list[RoundPlayOut] = []

    model_config = {"from_attributes": True}
