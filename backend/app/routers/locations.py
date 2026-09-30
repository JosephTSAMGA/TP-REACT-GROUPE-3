"""Routes CRUD des lieux. categoryId est obligatoire : un lieu a un thème."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import LocationCreate, LocationOut
from app.services.catalog import (
    CatalogError,
    create_location,
    delete_location,
    get_location,
    list_locations,
    update_location,
)

router = APIRouter(prefix="/api/locations", tags=["locations"])


def _http(exc: CatalogError) -> HTTPException:
    return HTTPException(status_code=exc.status_code, detail=exc.detail)


@router.get("", response_model=list[LocationOut])
def read_locations(
    # Filtre optionnel : seulement les lieux d'un thème.
    category_id: Optional[int] = Query(default=None, alias="categoryId"),
    db: Session = Depends(get_db),
) -> list[LocationOut]:
    try:
        locations = list_locations(db, category_id)
        return [LocationOut.model_validate(location) for location in locations]
    except CatalogError as exc:
        raise _http(exc) from exc


@router.post("", response_model=LocationOut, status_code=201)
def add_location(payload: LocationCreate, db: Session = Depends(get_db)) -> LocationOut:
    try:
        return LocationOut.model_validate(create_location(db, payload))
    except CatalogError as exc:
        raise _http(exc) from exc


@router.get("/{location_id}", response_model=LocationOut)
def read_location(location_id: int, db: Session = Depends(get_db)) -> LocationOut:
    try:
        return LocationOut.model_validate(get_location(db, location_id))
    except CatalogError as exc:
        raise _http(exc) from exc


@router.put("/{location_id}", response_model=LocationOut)
def replace_location(
    location_id: int,
    payload: LocationCreate,
    db: Session = Depends(get_db),
) -> LocationOut:
    try:
        return LocationOut.model_validate(update_location(db, location_id, payload))
    except CatalogError as exc:
        raise _http(exc) from exc


@router.delete("/{location_id}", status_code=204)
def remove_location(location_id: int, db: Session = Depends(get_db)) -> Response:
    try:
        delete_location(db, location_id)
    except CatalogError as exc:
        raise _http(exc) from exc
    return Response(status_code=204)
