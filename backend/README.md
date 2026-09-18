# Backend

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

`GET /health` est le seul endpoint implémenté. Routes de jeu : P3 (`docs/openapi.yaml`). Scoring : P2. Schémas : P1. Data : P4. Tests : P5. Voir `docs/CONSIGNES.md`.
