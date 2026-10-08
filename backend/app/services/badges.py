# =============================================================
# Logique métier : quels badges un joueur vient-il de débloquer ?
# Séparé du router pour que les règles restent testables sans passer
# par une vraie requête HTTP.
# =============================================================
import httpx
from sqlalchemy.orm import Session

from app.models.badge import Badge
from app.models.user import User
from app.models.user_badge import UserBadge
from app.schemas.badge import BadgeEvaluateRequest
from app.services.geocoding import reverse_geocode

FIRST_GAME_CODE = "premiere_partie"
FIVE_GAMES_CODE = "cinq_parties"
HIGH_SCORE_CODE = "voyageur_elite"
EXPLORER_CODE = "explorateur_international"

HIGH_SCORE_THRESHOLD = 20000


def _already_unlocked_codes(db: Session, user: User) -> set[str]:
    rows = (
        db.query(Badge.code)
        .join(UserBadge, UserBadge.badge_id == Badge.id)
        .filter(UserBadge.user_id == user.id)
        .all()
    )
    return {code for (code,) in rows}


def _unlock(
    db: Session, user: User, code: str, place: str | None = None
) -> UserBadge | None:
    badge = db.query(Badge).filter(Badge.code == code).first()
    if badge is None:
        # Le catalogue ne connaît pas ce code : rien à débloquer.
        return None
    user_badge = UserBadge(user_id=user.id, badge_id=badge.id, unlocked_place=place)
    db.add(user_badge)
    db.flush()  # obtient l'id généré sans committer tout de suite
    return user_badge


def evaluate_badges(
    db: Session, user: User, payload: BadgeEvaluateRequest
) -> list[UserBadge]:
    """Vérifie chaque règle de badge pour ce joueur et débloque celles
    désormais remplies. Renvoie uniquement les badges NOUVELLEMENT
    débloqués par cet appel (jamais les mêmes deux fois)."""
    already = _already_unlocked_codes(db, user)
    newly_unlocked: list[UserBadge] = []

    finished_sessions = [session for session in user.sessions if session.finished]
    best_score = max((session.score_total for session in finished_sessions), default=0)

    if FIRST_GAME_CODE not in already and len(finished_sessions) >= 1:
        unlocked = _unlock(db, user, FIRST_GAME_CODE)
        if unlocked is not None:
            newly_unlocked.append(unlocked)

    if FIVE_GAMES_CODE not in already and len(finished_sessions) >= 5:
        unlocked = _unlock(db, user, FIVE_GAMES_CODE)
        if unlocked is not None:
            newly_unlocked.append(unlocked)

    if HIGH_SCORE_CODE not in already and best_score >= HIGH_SCORE_THRESHOLD:
        unlocked = _unlock(db, user, HIGH_SCORE_CODE)
        if unlocked is not None:
            newly_unlocked.append(unlocked)

    if (
        EXPLORER_CODE not in already
        and payload.latitude is not None
        and payload.longitude is not None
    ):
        try:
            place = reverse_geocode(payload.latitude, payload.longitude)
        except (httpx.HTTPError, ValueError):
            # L'API externe est indisponible ou n'a rien trouvé : on ignore
            # simplement ce badge pour cet appel, sans faire échouer les autres.
            place = None
        if place is not None:
            unlocked = _unlock(db, user, EXPLORER_CODE, place=place)
            if unlocked is not None:
                newly_unlocked.append(unlocked)

    db.commit()
    for user_badge in newly_unlocked:
        db.refresh(user_badge)
    return newly_unlocked
