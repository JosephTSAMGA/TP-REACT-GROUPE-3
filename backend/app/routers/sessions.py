"""Génération d'une partie : 5 lieux au hasard, relisible ensuite."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import GameSession
from app.schemas import GameSessionOut, LocationOut, RandomSessionCreate
from app.services.catalog import CatalogError, create_random_session, get_session

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


def _http(exc: CatalogError) -> HTTPException:
    return HTTPException(status_code=exc.status_code, detail=exc.detail)


def _to_out(game_session: GameSession) -> GameSessionOut:
    return GameSessionOut(
        id=game_session.id,
        created_at=game_session.created_at,
        size=game_session.size,
        category_id=game_session.category_id,
        locations=[
            LocationOut.model_validate(entry.location) for entry in game_session.entries
        ],
    )


@router.post("/random", response_model=GameSessionOut, status_code=201)
def start_random_session(
    payload: RandomSessionCreate,
    db: Session = Depends(get_db),
) -> GameSessionOut:
    """Tire des lieux au hasard (5 par défaut) et ouvre une partie."""
    try:
        game_session = create_random_session(db, payload.size, payload.category_id)
    except CatalogError as exc:
        raise _http(exc) from exc
    return _to_out(game_session)


@router.get("/{session_id}", response_model=GameSessionOut)
def read_session(session_id: str, db: Session = Depends(get_db)) -> GameSessionOut:
    try:
        return _to_out(get_session(db, session_id))
    except CatalogError as exc:
        raise _http(exc) from exc
