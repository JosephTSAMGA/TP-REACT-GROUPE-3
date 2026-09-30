from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.models.user_badge import UserBadge
from app.schemas.badge import BadgeEvaluateRequest, UserBadgeOut, UserBadgeUpdate
from app.services.badges import evaluate_badges

router = APIRouter(prefix="/api/user-badges", tags=["user-badges"])


def _owned(user_badge_id: int, user: User, db: Session) -> UserBadge:
    row = (
        db.query(UserBadge)
        .options(selectinload(UserBadge.badge))
        .filter(UserBadge.id == user_badge_id)
        .first()
    )
    if row is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Déblocage introuvable.")
    if row.user_id != user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Ce n'est pas votre badge."
        )
    return row


@router.get("", response_model=list[UserBadgeOut])
def list_user_badges(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    return (
        db.query(UserBadge)
        .options(selectinload(UserBadge.badge))
        .filter(UserBadge.user_id == current_user.id)
        .order_by(UserBadge.id)
        .all()
    )


@router.post("", response_model=list[UserBadgeOut], status_code=status.HTTP_201_CREATED)
def create_user_badges(
    payload: BadgeEvaluateRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Création métier : évalue les règles et débloque les badges nouvellement gagnés."""
    return evaluate_badges(db, current_user, payload)


@router.get("/{user_badge_id}", response_model=UserBadgeOut)
def get_user_badge(
    user_badge_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return _owned(user_badge_id, current_user, db)


@router.patch("/{user_badge_id}", response_model=UserBadgeOut)
def update_user_badge(
    user_badge_id: int,
    payload: UserBadgeUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    row = _owned(user_badge_id, current_user, db)
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(row, field, value)
    db.commit()
    db.refresh(row)
    return row


@router.delete("/{user_badge_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_badge(
    user_badge_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    row = _owned(user_badge_id, current_user, db)
    db.delete(row)
    db.commit()
