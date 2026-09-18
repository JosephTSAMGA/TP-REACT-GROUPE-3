from fastapi import APIRouter

router = APIRouter(prefix="/api", tags=["game"])

# GET /api/round et POST /api/round/{roundId}/guess : P3
# Contrat : docs/openapi.yaml (ne pas renvoyer lat/lng avant le guess)
