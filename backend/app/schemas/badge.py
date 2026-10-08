from datetime import datetime

from pydantic import BaseModel, Field


class BadgeCreate(BaseModel):
    code: str = Field(min_length=2, max_length=50)
    name: str = Field(min_length=1, max_length=80)
    description: str = Field(min_length=1)


class BadgeOut(BaseModel):
    id: int
    code: str
    name: str
    description: str

    model_config = {"from_attributes": True}


class BadgeEvaluateRequest(BaseModel):
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)


class UserBadgeOut(BaseModel):
    id: int
    badge: BadgeOut
    unlocked_at: datetime
    unlocked_place: str | None = None

    model_config = {"from_attributes": True}


class UserBadgeUpdate(BaseModel):
    unlocked_place: str | None = Field(default=None, max_length=255)
