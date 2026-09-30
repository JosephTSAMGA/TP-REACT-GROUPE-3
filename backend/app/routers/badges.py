# =============================================================
# Routes /badges — catalogue public + badges du joueur connecté.
# Comme pour /sessions, le joueur concerné vient toujours du token JWT,
# jamais d'un id dans l'URL : impossible de consulter les badges d'un autre.
# =============================================================
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.badge import Badge
from app.models.user import User
from app.models.user_badge import UserBadge
from app.schemas.badge import BadgeEvaluateRequest, BadgeOut, UserBadgeOut
from app.services.badges import evaluate_badges

router = APIRouter(prefix="/badges", tags=["badges"])


@router.get("", response_model=list[BadgeOut])
def list_catalog(db: Session = Depends(get_db)):
    """Catalogue complet des badges existants. Public : ce n'est pas une
    donnée personnelle, seulement la liste des récompenses possibles."""
    return db.query(Badge).order_by(Badge.id).all()


@router.get("/me", response_model=list[UserBadgeOut])
def list_my_badges(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    """Badges déjà débloqués par le joueur connecté."""
    return (
        db.query(UserBadge)
        .filter(UserBadge.user_id == current_user.id)
        .order_by(UserBadge.unlocked_at)
        .all()
    )


@router.post("/evaluate", response_model=list[UserBadgeOut])
def evaluate(
    payload: BadgeEvaluateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Vérifie les règles de badges pour le joueur connecté et débloque
    celles désormais remplies. À appeler côté frontend après une partie
    terminée, avec la dernière position devinée si on veut tenter le
    badge Explorateur international."""
    return evaluate_badges(db, current_user, payload)
