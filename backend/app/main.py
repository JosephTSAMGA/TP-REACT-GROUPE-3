from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, SessionLocal, engine
import app.models  # noqa: F401
from app.routers import (
    auth,
    badges,
    categories,
    guesses,
    locations,
    rounds,
    sessions,
    user_badges,
    users,
)
from app.seed import seed_all

Base.metadata.create_all(bind=engine)

_seed_db = SessionLocal()
try:
    seed_all(_seed_db)
finally:
    _seed_db.close()

app = FastAPI(
    title="GetClose API",
    description=(
        "API FastAPI du jeu GetClose : comptes, parties, lieux, manches, "
        "guesses, scoring Haversine, badges et géocodage Nominatim."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


app.include_router(auth.router)
app.include_router(users.router)
app.include_router(sessions.router)
app.include_router(categories.router)
app.include_router(locations.router)
app.include_router(rounds.router)
app.include_router(guesses.router)
app.include_router(badges.router)
app.include_router(user_badges.router)
