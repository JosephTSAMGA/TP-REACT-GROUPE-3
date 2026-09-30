from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.game_session import GameSession
from app.models.user import User
from app.schemas.game_session import GameSessionOut, GameSessionUpdate
from app.services.catalog import CatalogError
from app.services.game import session_with_rounds, start_session, to_session_out

router = APIRouter(prefix="/api/sessions", tags=["sessions"])


def _owned(session_id: int, user: User, db: Session) -> GameSession:
    game_session = session_with_rounds(db, session_id)
    if game_session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partie introuvable.")
    if game_session.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Ce n'est pas votre partie."
        )
    return game_session


@router.post("", response_model=GameSessionOut, status_code=status.HTTP_201_CREATED)
def create_session(
    category_id: int | None = Query(default=None),
    size: int = Query(default=5, ge=1, le=20),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    try:
        game_session = start_session(
            db, current_user, category_id=category_id, size=size
        )
    except CatalogError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.detail) from exc
    return to_session_out(game_session)


@router.get("", response_model=list[GameSessionOut])
def list_my_sessions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    sessions = (
        db.query(GameSession)
        .filter(GameSession.user_id == current_user.id)
        .order_by(GameSession.id.desc())
        .all()
    )
    return [to_session_out(session_with_rounds(db, session.id) or session) for session in sessions]


@router.get("/{session_id}", response_model=GameSessionOut)
def get_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return to_session_out(_owned(session_id, current_user, db))


@router.patch("/{session_id}", response_model=GameSessionOut)
def update_session(
    session_id: int,
    payload: GameSessionUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    game_session = _owned(session_id, current_user, db)
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(game_session, field, value)
    if game_session.finished and game_session.finished_at is None:
        game_session.finished_at = datetime.now(timezone.utc)
    db.commit()
    loaded = session_with_rounds(db, game_session.id)
    assert loaded is not None
    return to_session_out(loaded)


@router.delete("/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(
    session_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    game_session = _owned(session_id, current_user, db)
    db.delete(game_session)
    db.commit()
