"""Routes CRUD des thèmes. Un thème qui a encore des lieux ne se supprime pas."""

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Category
from app.schemas import CategoryCreate, CategoryDetail, CategoryOut, LocationBrief
from app.services.catalog import (
    CatalogError,
    create_category,
    delete_category,
    get_category,
    list_categories,
    update_category,
)

router = APIRouter(prefix="/api/categories", tags=["categories"])


def _http(exc: CatalogError) -> HTTPException:
    return HTTPException(status_code=exc.status_code, detail=exc.detail)


def _to_out(category: Category) -> CategoryOut:
    return CategoryOut(
        id=category.id,
        name=category.name,
        slug=category.slug,
        location_count=len(category.locations),
    )


def _to_detail(category: Category) -> CategoryDetail:
    locations = sorted(category.locations, key=lambda location: location.name)
    return CategoryDetail(
        id=category.id,
        name=category.name,
        slug=category.slug,
        location_count=len(locations),
        locations=[LocationBrief.model_validate(location) for location in locations],
    )


@router.get("", response_model=list[CategoryOut])
def read_categories(db: Session = Depends(get_db)) -> list[CategoryOut]:
    return [_to_out(category) for category in list_categories(db)]


@router.post("", response_model=CategoryOut, status_code=201)
def add_category(payload: CategoryCreate, db: Session = Depends(get_db)) -> CategoryOut:
    try:
        return _to_out(create_category(db, payload))
    except CatalogError as exc:
        raise _http(exc) from exc


@router.get("/{category_id}", response_model=CategoryDetail)
def read_category(category_id: int, db: Session = Depends(get_db)) -> CategoryDetail:
    try:
        return _to_detail(get_category(db, category_id))
    except CatalogError as exc:
        raise _http(exc) from exc


@router.put("/{category_id}", response_model=CategoryOut)
def replace_category(
    category_id: int,
    payload: CategoryCreate,
    db: Session = Depends(get_db),
) -> CategoryOut:
    try:
        return _to_out(update_category(db, category_id, payload))
    except CatalogError as exc:
        raise _http(exc) from exc


@router.delete("/{category_id}", status_code=204)
def remove_category(category_id: int, db: Session = Depends(get_db)) -> Response:
    try:
        delete_category(db, category_id)
    except CatalogError as exc:
        raise _http(exc) from exc
    return Response(status_code=204)
