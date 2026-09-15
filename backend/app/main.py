from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import rounds

app = FastAPI(title="GeoGuessr TP", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5173", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rounds.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
