"""Règles métier du catalogue : catégories, lieux, slugs."""

import re
import unicodedata

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.models.category import Category
from app.models.location import Location
from app.schemas.category import CategoryCreate
from app.schemas.location import LocationCreate


class CatalogError(Exception):
    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")
    return slug or "categorie"


def list_categories(db: Session) -> list[Category]:
    return (
        db.query(Category)
        .options(selectinload(Category.locations))
        .order_by(Category.name)
        .all()
    )


def get_category(db: Session, category_id: int) -> Category:
    category = (
        db.query(Category)
        .options(selectinload(Category.locations))
        .filter(Category.id == category_id)
        .first()
    )
    if category is None:
        raise CatalogError(404, "Catégorie introuvable.")
    return category


def create_category(db: Session, payload: CategoryCreate) -> Category:
    category = Category(name=payload.name, slug=payload.slug or slugify(payload.name))
    db.add(category)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise CatalogError(409, "Une catégorie avec ce nom ou ce slug existe déjà.") from None
    return get_category(db, category.id)


def update_category(db: Session, category_id: int, payload: CategoryCreate) -> Category:
    category = get_category(db, category_id)
    category.name = payload.name
    category.slug = payload.slug or slugify(payload.name)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise CatalogError(409, "Une catégorie avec ce nom ou ce slug existe déjà.") from None
    return get_category(db, category_id)


def delete_category(db: Session, category_id: int) -> None:
    category = get_category(db, category_id)
    if category.locations:
        raise CatalogError(409, "Cette catégorie contient encore des lieux.")
    db.delete(category)
    db.commit()


def list_locations(db: Session, category_id: int | None) -> list[Location]:
    query = db.query(Location).options(selectinload(Location.category)).order_by(Location.name)
    if category_id is not None:
        if db.get(Category, category_id) is None:
            raise CatalogError(404, "Catégorie introuvable.")
        query = query.filter(Location.category_id == category_id)
    return query.all()


def get_location(db: Session, location_id: int) -> Location:
    location = (
        db.query(Location)
        .options(selectinload(Location.category))
        .filter(Location.id == location_id)
        .first()
    )
    if location is None:
        raise CatalogError(404, "Lieu introuvable.")
    return location


def _require_category(db: Session, category_id: int) -> Category:
    category = db.get(Category, category_id)
    if category is None:
        raise CatalogError(404, "Catégorie introuvable.")
    return category


def create_location(db: Session, payload: LocationCreate) -> Location:
    _require_category(db, payload.category_id)
    location = Location(
        name=payload.name,
        latitude=payload.latitude,
        longitude=payload.longitude,
        image_url=payload.image_url,
        category_id=payload.category_id,
    )
    db.add(location)
    db.commit()
    return get_location(db, location.id)


def update_location(db: Session, location_id: int, payload: LocationCreate) -> Location:
    location = get_location(db, location_id)
    _require_category(db, payload.category_id)
    location.name = payload.name
    location.latitude = payload.latitude
    location.longitude = payload.longitude
    location.image_url = payload.image_url
    location.category_id = payload.category_id
    db.commit()
    return get_location(db, location_id)


def delete_location(db: Session, location_id: int) -> None:
    location = get_location(db, location_id)
    if location.rounds:
        raise CatalogError(409, "Ce lieu est encore utilisé dans une manche.")
    db.delete(location)
    db.commit()
