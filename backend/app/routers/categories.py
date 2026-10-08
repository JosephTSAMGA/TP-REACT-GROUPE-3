from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schemas.category import CategoryCreate, CategoryDetail, CategoryOut, LocationBrief
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


def _to_out(category) -> CategoryOut:
    return CategoryOut(
        id=category.id,
        name=category.name,
        slug=category.slug,
        location_count=len(category.locations),
    )


@router.get("", response_model=list[CategoryOut])
def read_categories(db: Session = Depends(get_db)):
    return [_to_out(category) for category in list_categories(db)]


@router.post("", response_model=CategoryOut, status_code=201)
def add_category(
    payload: CategoryCreate,
    _user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return _to_out(create_category(db, payload))
    except CatalogError as exc:
        raise _http(exc) from exc


@router.get("/{category_id}", response_model=CategoryDetail)
def read_category(category_id: int, db: Session = Depends(get_db)):
    try:
        category = get_category(db, category_id)
    except CatalogError as exc:
        raise _http(exc) from exc
    locations = sorted(category.locations, key=lambda item: item.name)
    return CategoryDetail(
        id=category.id,
        name=category.name,
        slug=category.slug,
        location_count=len(locations),
        locations=[LocationBrief.model_validate(item) for item in locations],
    )


@router.put("/{category_id}", response_model=CategoryOut)
def replace_category(
    category_id: int,
    payload: CategoryCreate,
    _user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        return _to_out(update_category(db, category_id, payload))
    except CatalogError as exc:
        raise _http(exc) from exc


@router.delete("/{category_id}", status_code=204)
def remove_category(
    category_id: int,
    _user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        delete_category(db, category_id)
    except CatalogError as exc:
        raise _http(exc) from exc
    return Response(status_code=204)
