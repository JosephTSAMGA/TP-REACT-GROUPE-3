# =============================================================
# Point d'entrée de l'application FastAPI.
# Ce fichier reste volontairement court : il ne fait que créer l'app
# et brancher les routers de chaque ressource. La vraie logique vit
# dans routers/ (routes HTTP) et services/ (logique métier).
# =============================================================
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, SessionLocal, engine

# Crée les tables en base si elles n'existent pas encore (simple pour un
# projet étudiant ; un vrai projet utiliserait des migrations Alembic).
# Importer les modèles avant ce create_all est indispensable : SQLAlchemy
# ne connaît une table que si sa classe Python a été chargée au moins une fois.
from app.models import badge, game_session, user, user_badge  # noqa: F401
from app.routers import auth, badges, sessions
from app.seed_badges import seed_badges_if_empty

Base.metadata.create_all(bind=engine)

# Remplit le catalogue de badges une fois, si la table vient d'être créée.
_seed_db = SessionLocal()
try:
    seed_badges_if_empty(_seed_db)
finally:
    _seed_db.close()

app = FastAPI(
    title="GetClose API",
    description="API backend du jeu de géographie GetClose — comptes joueurs, "
    "parties, manches, score et classement.",
    version="0.1.0",
)

# Autorise le frontend React (en dev, sur localhost) à appeler cette API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    """Route simple pour vérifier que l'API répond, sans toucher à la DB."""
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(sessions.router)
app.include_router(badges.router)

# À mesure que chaque étudiant crée son router, on le branche ici, par exemple :
# from app.routers import locations, categories
# app.include_router(locations.router)
# app.include_router(categories.router)
