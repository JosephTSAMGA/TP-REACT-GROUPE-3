from pydantic import BaseModel, Field, field_validator


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    slug: str | None = Field(default=None, max_length=80, pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Le nom est obligatoire.")
        return stripped


class CategoryOut(BaseModel):
    id: int
    name: str
    slug: str
    location_count: int = 0

    model_config = {"from_attributes": True}


class LocationBrief(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    image_url: str
    category_id: int

    model_config = {"from_attributes": True}


class CategoryDetail(CategoryOut):
    locations: list[LocationBrief] = []
