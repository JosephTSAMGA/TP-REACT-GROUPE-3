"""Règles métier : slug, appartenance à une catégorie, tirage d'une partie."""

import random
import re
import unicodedata
import uuid
from datetime import datetime
from typing import Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.models import Category, GameSession, GameSessionLocation, Location
from app.schemas import CategoryCreate, LocationCreate


class CatalogError(Exception):
    """Erreur métier traduite en HTTP par les routers (404, 409, 422)."""

    def __init__(self, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(detail)


def slugify(value: str) -> str:
    # "Cathédrale" devient "cathedrale" : un slug sans accent, stable en URL.
    normalized = unicodedata.normalize("NFKD", value)
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    slug = re.sub(r"[^a-z0-9]+", "-", ascii_text.lower()).strip("-")
    return slug or "categorie"


def list_categories(db: Session) -> list[Category]:
    stmt = (
        select(Category)
        .options(selectinload(Category.locations))
        .order_by(Category.name)
    )
    return list(db.scalars(stmt).all())


def get_category(db: Session, category_id: int) -> Category:
    stmt = (
        select(Category)
        .options(selectinload(Category.locations))
        .where(Category.id == category_id)
    )
    category = db.scalar(stmt)
    if category is None:
        raise CatalogError(404, "Catégorie introuvable.")
    return category


def create_category(db: Session, payload: CategoryCreate) -> Category:
    # Slug fourni par le client, sinon déduit du nom.
    category = Category(name=payload.name, slug=payload.slug or slugify(payload.name))
    db.add(category)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise CatalogError(
            409,
            "Une catégorie avec ce nom ou ce slug existe déjà.",
        ) from None
    return get_category(db, category.id)


def update_category(db: Session, category_id: int, payload: CategoryCreate) -> Category:
    category = get_category(db, category_id)
    category.name = payload.name
    category.slug = payload.slug or slugify(payload.name)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise CatalogError(
            409,
            "Une catégorie avec ce nom ou ce slug existe déjà.",
        ) from None
    return get_category(db, category_id)


def delete_category(db: Session, category_id: int) -> None:
    category = get_category(db, category_id)
    # On refuse plutôt que de supprimer les lieux en cascade :
    # ils n'auraient plus de thème.
    if category.locations:
        raise CatalogError(409, "Cette catégorie contient encore des lieux.")
    db.delete(category)
    db.commit()


def _location_query():
    # Charge la catégorie en même temps : la réponse JSON l'inclut.
    return select(Location).options(selectinload(Location.category))


def list_locations(db: Session, category_id: Optional[int]) -> list[Location]:
    stmt = _location_query().order_by(Location.name)
    if category_id is not None:
        if db.get(Category, category_id) is None:
            raise CatalogError(404, "Catégorie introuvable.")
        stmt = stmt.where(Location.category_id == category_id)
    return list(db.scalars(stmt).all())


def get_location(db: Session, location_id: int) -> Location:
    location = db.scalar(_location_query().where(Location.id == location_id))
    if location is None:
        raise CatalogError(404, "Lieu introuvable.")
    return location


def _require_category(db: Session, category_id: int) -> Category:
    category = db.get(Category, category_id)
    if category is None:
        raise CatalogError(404, "Catégorie introuvable.")
    return category


def create_location(db: Session, payload: LocationCreate) -> Location:
    # Un lieu sans catégorie valide n'est pas enregistré.
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
    db.delete(location)
    db.commit()


def _session_query():
    return select(GameSession).options(
        selectinload(GameSession.entries)
        .selectinload(GameSessionLocation.location)
        .selectinload(Location.category)
    )


def get_session(db: Session, session_id: str) -> GameSession:
    game_session = db.scalar(_session_query().where(GameSession.id == session_id))
    if game_session is None:
        raise CatalogError(404, "Partie introuvable.")
    return game_session


def create_random_session(
    db: Session,
    size: int,
    category_id: Optional[int],
) -> GameSession:
    """Choisit `size` lieux distincts au hasard et enregistre la partie."""
    stmt = _location_query()
    if category_id is not None:
        _require_category(db, category_id)
        stmt = stmt.where(Location.category_id == category_id)

    locations = list(db.scalars(stmt).all())
    # Mieux vaut refuser que de renvoyer une partie incomplète.
    if len(locations) < size:
        raise CatalogError(
            422,
            f"Pas assez de lieux ({len(locations)}) pour une partie de {size} manches.",
        )

    # sample (pas choice) : chaque lieu n'apparaît qu'une fois dans la partie.
    picked = random.sample(locations, size)
    game_session = GameSession(
        id=str(uuid.uuid4()),
        created_at=datetime.utcnow(),
        size=size,
        category_id=category_id,
    )
    # position fige l'ordre du tirage : GET /sessions/{id} renvoie le même ordre.
    game_session.entries = [
        GameSessionLocation(location=location, position=index)
        for index, location in enumerate(picked)
    ]
    db.add(game_session)
    db.commit()
    return get_session(db, game_session.id)
