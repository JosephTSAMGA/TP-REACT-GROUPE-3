# =============================================================
# Remplit le catalogue de badges au démarrage, une seule fois.
# =============================================================
from sqlalchemy.orm import Session

from app.models.badge import Badge

CATALOG: list[tuple[str, str, str]] = [
    ("premiere_partie", "Premier voyage", "Terminer sa première partie."),
    ("cinq_parties", "Grand voyageur", "Terminer 5 parties."),
    (
        "voyageur_elite",
        "Voyageur d'élite",
        "Atteindre un score total de 20000 ou plus sur une partie.",
    ),
    (
        "explorateur_international",
        "Explorateur international",
        "Faire identifier un lieu deviné via la géolocalisation inversée.",
    ),
]


def seed_badges_if_empty(db: Session) -> None:
    if db.query(Badge).first() is not None:
        return
    for code, name, description in CATALOG:
        db.add(Badge(code=code, name=name, description=description))
    db.commit()
