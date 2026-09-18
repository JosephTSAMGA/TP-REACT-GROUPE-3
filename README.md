# TP React Groupe 3 — GeoGuessr

React + TypeScript / FastAPI.  
À lire en premier : [docs/CONSIGNES.md](docs/CONSIGNES.md)  
Architecture : [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) · Contrat API : [docs/api.md](docs/api.md)

## Prérequis

- Node.js 20+
- Python 3.9+ (3.12 recommandé)

## Lancer le projet

```bash
git clone <url-du-repo>
cd TP-REACT-GROUPE-3
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Ouvre [http://127.0.0.1:5173](http://127.0.0.1:5173).

### Backend

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Santé : [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)  
Docs générées : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

Les routes de jeu sont dans le contrat, **pas encore implémentées**. Qui fait quoi : [docs/CONSIGNES.md](docs/CONSIGNES.md).

## Qui fait quoi (résumé)

| | Front | Back |
|---|---|---|
| P1 | `features/game` | `schemas.py` |
| P2 | `features/map` (Leaflet) | `scoring.py` |
| P3 | `shared/api` | routes + `game.py` + `/static` |
| P4 | `<img imageUrl>` | `data/` json + images |
| P5 | coller P1+P2, CI | tests |

Branches : [CONTRIBUTING.md](CONTRIBUTING.md).
