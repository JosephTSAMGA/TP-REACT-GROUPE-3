from datetime import datetime

from pydantic import BaseModel, Field


class GuessCreate(BaseModel):
    round_id: int
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class GuessUpdate(BaseModel):
    latitude: float | None = Field(default=None, ge=-90, le=90)
    longitude: float | None = Field(default=None, ge=-180, le=180)


class ActualLocationOut(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    image_url: str

    model_config = {"from_attributes": True}


class GuessOut(BaseModel):
    id: int
    round_id: int
    user_id: int
    latitude: float
    longitude: float
    distance_km: float
    score: int
    created_at: datetime
    actual_location: ActualLocationOut

    model_config = {"from_attributes": True}
