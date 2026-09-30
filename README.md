# GetClose — TP React + FastAPI (groupe 4)

Front React (GetClose) + API FastAPI (JWT, 8 CRUD).  
Swagger : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

**Docker n’est pas obligatoire.** Sans Docker, l’API utilise SQLite. Docker ne sert que si vous voulez PostgreSQL (recommandé pour coller à la grille).

## Lancer le projet

### Backend (sans Docker)

```bash
cd backend
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

### Backend (PostgreSQL + Docker, optionnel)

```bash
cd backend
copy .env.example .env
# Dans .env, décommentez la ligne DATABASE_URL postgresql
docker compose up -d db
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Santé : [http://127.0.0.1:8000/health](http://127.0.0.1:8000/health)

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Ouvre [http://127.0.0.1:5173](http://127.0.0.1:5173). Vite proxy `/api` vers le backend.

## Tests API

```bash
cd backend
pytest
```

## Répartition

| Personne | Front | Back |
|---|---|---|
| P1 | Accueil, routes | User, GameSession, JWT |
| P2 | Carte, manches | — (consomme Round / Guess) |
| P3 / lieux | Résultat, Nominatim | Category, Location, tirage |
| P4 | Badges (API) | Badge, UserBadge |
| P5 | Historique | Round, Guess, scoring |

Le jeu enchaîne : inscription/connexion → `POST /api/sessions` → clic carte → `POST /api/guesses` → résultat.
