"""Création d'une partie : tirage de lieux et création des manches."""

import random

from sqlalchemy.orm import Session, selectinload

from app.models.category import Category
from app.models.game_session import GameSession
from app.models.guess import Guess
from app.models.location import Location
from app.models.round import Round
from app.models.user import User
from app.schemas.game_session import GameSessionOut, RoundPlayOut
from app.schemas.guess import ActualLocationOut, GuessOut
from app.schemas.round import RoundOut
from app.services.catalog import CatalogError


def session_with_rounds(db: Session, session_id: int) -> GameSession | None:
    return (
        db.query(GameSession)
        .options(selectinload(GameSession.rounds).selectinload(Round.location))
        .filter(GameSession.id == session_id)
        .first()
    )


def start_session(
    db: Session,
    user: User,
    *,
    category_id: int | None = None,
    size: int = 5,
) -> GameSession:
    query = db.query(Location)
    if category_id is not None:
        if db.get(Category, category_id) is None:
            raise CatalogError(404, "Catégorie introuvable.")
        query = query.filter(Location.category_id == category_id)

    locations = query.all()
    if len(locations) < size:
        raise CatalogError(
            422,
            f"Pas assez de lieux ({len(locations)}) pour une partie de {size} manches.",
        )

    picked = random.sample(locations, size)
    game_session = GameSession(
        user_id=user.id,
        category_id=category_id,
        size=size,
    )
    db.add(game_session)
    db.flush()

    for index, location in enumerate(picked):
        db.add(
            Round(
                session_id=game_session.id,
                location_id=location.id,
                position=index,
            )
        )
    db.commit()
    loaded = session_with_rounds(db, game_session.id)
    assert loaded is not None
    return loaded


def to_round_play(round_: Round) -> RoundPlayOut:
    return RoundPlayOut(
        id=round_.id,
        session_id=round_.session_id,
        position=round_.position,
        image_url=round_.location.image_url,
        guessed=round_.guessed,
    )


def to_round_out(round_: Round) -> RoundOut:
    return RoundOut(
        id=round_.id,
        session_id=round_.session_id,
        location_id=round_.location_id,
        position=round_.position,
        image_url=round_.location.image_url,
        guessed=round_.guessed,
    )


def to_session_out(session: GameSession) -> GameSessionOut:
    return GameSessionOut(
        id=session.id,
        user_id=session.user_id,
        category_id=session.category_id,
        size=session.size,
        score_total=session.score_total,
        finished=session.finished,
        started_at=session.started_at,
        finished_at=session.finished_at,
        rounds=[to_round_play(round_) for round_ in session.rounds],
    )


def to_guess_out(guess: Guess) -> GuessOut:
    location = guess.round.location
    return GuessOut(
        id=guess.id,
        round_id=guess.round_id,
        user_id=guess.user_id,
        latitude=guess.latitude,
        longitude=guess.longitude,
        distance_km=guess.distance_km,
        score=guess.score,
        created_at=guess.created_at,
        actual_location=ActualLocationOut.model_validate(location),
    )
