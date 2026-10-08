from pydantic import BaseModel, Field


class RoundCreate(BaseModel):
    session_id: int
    location_id: int
    position: int = Field(ge=0)


class RoundUpdate(BaseModel):
    location_id: int | None = None
    position: int | None = Field(default=None, ge=0)


class RoundOut(BaseModel):
    id: int
    session_id: int
    location_id: int
    position: int
    image_url: str
    guessed: bool

    model_config = {"from_attributes": True}
