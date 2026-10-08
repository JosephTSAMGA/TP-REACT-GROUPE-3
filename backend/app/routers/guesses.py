from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.guess import Guess
from app.models.round import Round
from app.models.user import User
from app.schemas.guess import GuessCreate, GuessOut, GuessUpdate
from app.services.game import to_guess_out
from app.services.scoring import distance_km, score_from_distance_km

router = APIRouter(prefix="/api/guesses", tags=["guesses"])


def _load_guess(guess_id: int, db: Session) -> Guess | None:
    return (
        db.query(Guess)
        .options(
            selectinload(Guess.round).selectinload(Round.location),
            selectinload(Guess.round).selectinload(Round.session),
        )
        .filter(Guess.id == guess_id)
        .first()
    )


def _owned_guess(guess_id: int, user: User, db: Session) -> Guess:
    guess = _load_guess(guess_id, db)
    if guess is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Guess introuvable.")
    if guess.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Ce n'est pas votre guess."
        )
    return guess


def _apply_score(guess: Guess, round_: Round) -> None:
    location = round_.location
    guess.distance_km = distance_km(
        guess.latitude, guess.longitude, location.latitude, location.longitude
    )
    guess.score = score_from_distance_km(guess.distance_km)


@router.post("", response_model=GuessOut, status_code=status.HTTP_201_CREATED)
def create_guess(
    payload: GuessCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    round_ = (
        db.query(Round)
        .options(selectinload(Round.location), selectinload(Round.session))
        .filter(Round.id == payload.round_id)
        .first()
    )
    if round_ is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Manche introuvable.")
    if round_.session.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Cette manche ne vous appartient pas."
        )
    if round_.guessed or round_.guess is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Un guess a déjà été soumis pour cette manche.",
        )

    guess = Guess(
        round_id=round_.id,
        user_id=current_user.id,
        latitude=payload.latitude,
        longitude=payload.longitude,
    )
    _apply_score(guess, round_)
    round_.guessed = True
    round_.session.score_total += guess.score
    db.add(guess)
    db.commit()
    return to_guess_out(_owned_guess(guess.id, current_user, db))


@router.get("", response_model=list[GuessOut])
def list_guesses(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    guesses = (
        db.query(Guess)
        .options(selectinload(Guess.round).selectinload(Round.location))
        .filter(Guess.user_id == current_user.id)
        .order_by(Guess.id)
        .all()
    )
    return [to_guess_out(guess) for guess in guesses]


@router.get("/{guess_id}", response_model=GuessOut)
def get_guess(
    guess_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return to_guess_out(_owned_guess(guess_id, current_user, db))


@router.patch("/{guess_id}", response_model=GuessOut)
def update_guess(
    guess_id: int,
    payload: GuessUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    guess = _owned_guess(guess_id, current_user, db)
    previous_score = guess.score
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(guess, field, value)
    _apply_score(guess, guess.round)
    guess.round.session.score_total += guess.score - previous_score
    db.commit()
    return to_guess_out(_owned_guess(guess.id, current_user, db))


@router.delete("/{guess_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_guess(
    guess_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    guess = _owned_guess(guess_id, current_user, db)
    guess.round.guessed = False
    guess.round.session.score_total = max(0, guess.round.session.score_total - guess.score)
    db.delete(guess)
    db.commit()
