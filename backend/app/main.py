from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app import database
from app.routers import categories, locations, rounds, sessions
from app.seed import seed_if_empty


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # On passe par le module : un `from app.database import SessionLocal`
    # figerait None, la valeur au moment de l'import.
    database.configure()
    assert database.SessionLocal is not None
    db = database.SessionLocal()
    try:
        seed_if_empty(db)
    finally:
        db.close()
    yield


app = FastAPI(title="GeoGuessr TP", version="0.1.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rounds.router)
# Lieux, catégories et tirage aléatoire d'une partie.
app.include_router(categories.router)
app.include_router(locations.router)
app.include_router(sessions.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
