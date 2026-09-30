from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.database import get_db
from app.models.badge import Badge
from app.models.user import User
from app.schemas.badge import BadgeCreate, BadgeEvaluateRequest, BadgeOut, UserBadgeOut
from app.services.badges import evaluate_badges

router = APIRouter(prefix="/api/badges", tags=["badges"])


@router.get("", response_model=list[BadgeOut])
def list_catalog(db: Session = Depends(get_db)):
    return db.query(Badge).order_by(Badge.id).all()


@router.post("", response_model=BadgeOut, status_code=status.HTTP_201_CREATED)
def create_badge(
    payload: BadgeCreate,
    _user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if db.query(Badge).filter(Badge.code == payload.code).first():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ce code de badge existe déjà.")
    badge = Badge(code=payload.code, name=payload.name, description=payload.description)
    db.add(badge)
    db.commit()
    db.refresh(badge)
    return badge


@router.get("/me", response_model=list[UserBadgeOut])
def list_my_badges(
    current_user: User = Depends(get_current_user), db: Session = Depends(get_db)
):
    from app.models.user_badge import UserBadge

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
    return evaluate_badges(db, current_user, payload)


@router.get("/{badge_id}", response_model=BadgeOut)
def read_badge(badge_id: int, db: Session = Depends(get_db)):
    badge = db.query(Badge).filter(Badge.id == badge_id).first()
    if badge is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Badge introuvable.")
    return badge


@router.put("/{badge_id}", response_model=BadgeOut)
def replace_badge(
    badge_id: int,
    payload: BadgeCreate,
    _user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    badge = db.query(Badge).filter(Badge.id == badge_id).first()
    if badge is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Badge introuvable.")
    duplicate = (
        db.query(Badge).filter(Badge.code == payload.code, Badge.id != badge_id).first()
    )
    if duplicate:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Ce code de badge existe déjà.")
    badge.code = payload.code
    badge.name = payload.name
    badge.description = payload.description
    db.commit()
    db.refresh(badge)
    return badge


@router.delete("/{badge_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_badge(
    badge_id: int,
    _user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    badge = db.query(Badge).filter(Badge.id == badge_id).first()
    if badge is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Badge introuvable.")
    db.delete(badge)
    db.commit()
