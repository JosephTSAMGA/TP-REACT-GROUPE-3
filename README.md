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

Les routes FastAPI du contrat ne sont pas le sujet de l’oral front. Le jeu tourne **dans le navigateur** (Nominatim + localStorage).

## Qui fait quoi

| | Front |
|---|---|
| P1 | routes, NavBar, StartScreen |
| P2 | GamePage, RoundScreen, carte Leaflet |
| P3 | scoring, geocoding Nominatim, RoundResult |
| P5 | FinishedScreen, historique, localStorage |

Branches : [CONTRIBUTING.md](CONTRIBUTING.md).
