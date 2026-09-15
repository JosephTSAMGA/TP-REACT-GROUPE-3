# Backend

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

`GET /health` est le seul endpoint implémenté. Les routes de jeu suivent `docs/openapi.yaml`.

Images (P4) : `app/data/images/`, à servir plus tard en `/static/locations/` (P3). Voir `docs/CONSIGNES.md`.
