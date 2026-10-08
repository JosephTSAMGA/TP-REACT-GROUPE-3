from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.location import LocationCreate, LocationOut
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
    category_id: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    try:
        return [LocationOut.model_validate(item) for item in list_locations(db, category_id)]
    except CatalogError as exc:
        raise _http(exc) from exc


@router.post("", response_model=LocationOut, status_code=201)
def add_location(
    payload: LocationCreate,
    _user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return LocationOut.model_validate(create_location(db, payload))
    except CatalogError as exc:
        raise _http(exc) from exc


@router.get("/{location_id}", response_model=LocationOut)
def read_location(location_id: int, db: Session = Depends(get_db)):
    try:
        return LocationOut.model_validate(get_location(db, location_id))
    except CatalogError as exc:
        raise _http(exc) from exc


@router.put("/{location_id}", response_model=LocationOut)
def replace_location(
    location_id: int,
    payload: LocationCreate,
    _user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return LocationOut.model_validate(update_location(db, location_id, payload))
    except CatalogError as exc:
        raise _http(exc) from exc


@router.delete("/{location_id}", status_code=204)
def remove_location(
    location_id: int,
    _user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        delete_location(db, location_id)
    except CatalogError as exc:
        raise _http(exc) from exc
    return Response(status_code=204)
