from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session, selectinload

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.game_session import GameSession
from app.models.location import Location
from app.models.round import Round
from app.models.user import User
from app.schemas.round import RoundCreate, RoundOut, RoundUpdate
from app.services.game import to_round_out

router = APIRouter(prefix="/api/rounds", tags=["rounds"])


def _owned_round(round_id: int, user: User, db: Session) -> Round:
    round_ = (
        db.query(Round)
        .options(selectinload(Round.location), selectinload(Round.session))
        .filter(Round.id == round_id)
        .first()
    )
    if round_ is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manche introuvable.")
    if round_.session.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Cette manche ne vous appartient pas."
        )
    return round_


@router.post("", response_model=RoundOut, status_code=status.HTTP_201_CREATED)
def create_round(
    payload: RoundCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    session = db.query(GameSession).filter(GameSession.id == payload.session_id).first()
    if session is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Partie introuvable.")
    if session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Ce n'est pas votre partie."
        )
    if db.get(Location, payload.location_id) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lieu introuvable.")
    existing = (
        db.query(Round)
        .filter(Round.session_id == payload.session_id, Round.position == payload.position)
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Une manche existe déjà à cette position.",
        )

    round_ = Round(
        session_id=payload.session_id,
        location_id=payload.location_id,
        position=payload.position,
    )
    db.add(round_)
    db.commit()
    db.refresh(round_)
    round_ = _owned_round(round_.id, current_user, db)
    return to_round_out(round_)


@router.get("", response_model=list[RoundOut])
def list_rounds(
    session_id: int | None = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = (
        db.query(Round)
        .options(selectinload(Round.location), selectinload(Round.session))
        .join(GameSession)
        .filter(GameSession.user_id == current_user.id)
    )
    if session_id is not None:
        query = query.filter(Round.session_id == session_id)
    return [to_round_out(round_) for round_ in query.order_by(Round.id).all()]


@router.get("/{round_id}", response_model=RoundOut)
def get_round(
    round_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return to_round_out(_owned_round(round_id, current_user, db))


@router.patch("/{round_id}", response_model=RoundOut)
def update_round(
    round_id: int,
    payload: RoundUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    round_ = _owned_round(round_id, current_user, db)
    if round_.guessed:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Impossible de modifier une manche déjà jouée.",
        )
    updates = payload.model_dump(exclude_unset=True)
    if "location_id" in updates and db.get(Location, updates["location_id"]) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lieu introuvable.")
    for field, value in updates.items():
        setattr(round_, field, value)
    db.commit()
    return to_round_out(_owned_round(round_.id, current_user, db))


@router.delete("/{round_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_round(
    round_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    round_ = _owned_round(round_id, current_user, db)
    db.delete(round_)
    db.commit()
