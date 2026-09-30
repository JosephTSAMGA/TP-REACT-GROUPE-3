"""Schémas JSON des ressources Category, Location et des parties aléatoires."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class APIModel(BaseModel):
    # from_attributes : le JSON peut venir d'un objet SQLAlchemy.
    # populate_by_name : le front envoie imageUrl, Python stocke image_url.
    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class CategoryCreate(APIModel):
    name: str = Field(min_length=1, max_length=80)
    slug: Optional[str] = Field(
        default=None,
        max_length=80,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
    )

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        stripped = value.strip()
        if not stripped:
            raise ValueError("Le nom est obligatoire.")
        return stripped


class CategoryUpdate(CategoryCreate):
    pass


class CategoryBrief(APIModel):
    id: int
    name: str
    slug: str


class CategoryOut(CategoryBrief):
    # Compteur pour l'accueil : on sait si un thème a assez de lieux.
    location_count: int = Field(alias="locationCount")


class LocationCreate(APIModel):
    name: str = Field(min_length=1, max_length=120)
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)
    image_url: str = Field(alias="imageUrl", min_length=1, max_length=500)
    category_id: int = Field(alias="categoryId")

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


class LocationUpdate(LocationCreate):
    pass


class LocationBrief(APIModel):
    id: int
    name: str
    latitude: float
    longitude: float
    image_url: str = Field(alias="imageUrl")
    category_id: int = Field(alias="categoryId")


class LocationOut(LocationBrief):
    # La catégorie est incluse pour montrer la relation, pas seulement l'id.
    category: CategoryBrief


class CategoryDetail(CategoryOut):
    locations: list[LocationBrief]


class RandomSessionCreate(APIModel):
    # 5 manches, comme le reste du jeu. categoryId vide = tous les thèmes.
    size: int = Field(default=5, ge=1, le=20)
    category_id: Optional[int] = Field(default=None, alias="categoryId")


class GameSessionOut(APIModel):
    id: str
    created_at: datetime = Field(alias="createdAt")
    size: int
    category_id: Optional[int] = Field(default=None, alias="categoryId")
    locations: list[LocationOut]
