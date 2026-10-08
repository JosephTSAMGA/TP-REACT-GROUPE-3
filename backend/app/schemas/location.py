from pydantic import BaseModel, Field, field_validator


class LocationCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    image_url: str = Field(min_length=1, max_length=500)
    category_id: int

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Le nom est obligatoire.")
        return stripped

    @field_validator("image_url")
    @classmethod
    def http_url(cls, value: str) -> str:
        if not value.startswith(("http://", "https://")):
            raise ValueError("L'URL de l'image doit commencer par http:// ou https://.")
        return value


class CategoryBrief(BaseModel):
    id: int
    name: str
    slug: str

    model_config = {"from_attributes": True}


class LocationOut(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    image_url: str
    category_id: int
    category: CategoryBrief

    model_config = {"from_attributes": True}
