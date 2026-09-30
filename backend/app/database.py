"""SQLite + sessions SQLAlchemy.

La base est un fichier local, créé au démarrage. Les tests
remplacent l'URL pour ne pas écrire dans le fichier de dev.
"""

import os
from collections.abc import Generator
from pathlib import Path
from typing import Optional

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import Session, sessionmaker

from app.models import Base

# Fichier par défaut, ignoré par git : backend/app/data/geoguessr.db.
_DEFAULT_PATH = Path(__file__).resolve().parent / "data" / "geoguessr.db"

# None tant que configure() n'a pas tourné. On les lit sur le module
# (app.database.SessionLocal), pas via un import figé à None.
engine: Optional[Engine] = None
SessionLocal: Optional[sessionmaker] = None


def database_url() -> str:
    # DATABASE_URL sert surtout aux tests (base temporaire).
    configured = os.environ.get("DATABASE_URL")
    if configured:
        return configured
    return f"sqlite:///{_DEFAULT_PATH}"


def configure(url: Optional[str] = None) -> None:
    """Ouvre le moteur et crée les tables qui manquent."""
    global engine, SessionLocal
    # Ferme l'ancien moteur si on change de fichier (cas des tests).
    if engine is not None:
        engine.dispose()

    resolved = url or database_url()
    # TestClient appelle la base depuis un autre thread que la requête.
    connect_args = {"check_same_thread": False} if resolved.startswith("sqlite") else {}
    engine = create_engine(resolved, connect_args=connect_args)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    # create_all n'efface rien : une base déjà remplie est laissée telle quelle.
    Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    # Une session par requête HTTP, fermée même si la route lève une erreur.
    if SessionLocal is None:
        configure()
    assert SessionLocal is not None
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@event.listens_for(Engine, "connect")
def _enable_sqlite_foreign_keys(dbapi_connection, _connection_record) -> None:
    # SQLite ignore les clés étrangères par défaut. Sans ce pragma,
    # un lieu pourrait référencer une catégorie qui n'existe pas.
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
