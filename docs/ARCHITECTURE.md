# Architecture — GetClose

Monorepo `frontend/` (Vite + React + TypeScript) + `backend/` (FastAPI).

## Décisions

| Sujet | Choix |
|---|---|
| Front | React, React Router, Leaflet / OSM |
| Back | FastAPI, SQLAlchemy, Pydantic v2 |
| Auth | JWT (`/api/auth/register`, `/api/auth/login`) |
| Base | SQLite par défaut ; PostgreSQL optionnel (`docker compose`) |
| État de partie | Persisté en base (`GameSession` + `Round` + `Guess`) |
| Score | Haversine **côté serveur** |
| API tierce | Nominatim (reverse geocoding), appelée par FastAPI pour les badges et par le front pour l’écran résultat |
| Photos | URLs Wikimedia dans `locations.image_url` (seed `app/seed.py`) |

## Frontend

```
frontend/src/
  app/                 # routes, NavBar
  features/
    game/              # StartScreen, GamePage, RoundScreen
    map/               # InteractiveMap (Leaflet)
    result/            # RoundResult
    history/           # FinishedScreen, HistoryScreen
  shared/
    api/               # client JWT (sessions, guesses)
    types.ts
```

Le front n’orchestre plus 5 manches « dans le vide » : `POST /api/sessions` crée la partie, `POST /api/guesses` enregistre le clic.

## Backend

```
backend/app/
  main.py
  database.py
  core/                # config, JWT, get_current_user
  models/              # 8 tables
  schemas/             # Pydantic
  routers/             # HTTP léger
  services/            # scoring, catalogue, badges, geocoding
  seed.py
```

Séparation : routers → services → models. Les routes restent minces.

### 8 ressources CRUD

User, GameSession, Category, Location, Round, Guess, Badge, UserBadge.

### Relations

- User 1–N GameSession
- GameSession 1–N Round
- Round 1–1 Guess
- Category 1–N Location
- Location 1–N Round
- User N–N Badge via UserBadge

### Fonctionnalités avancées

1. Tirage d’une partie (`POST /api/sessions` : 5 lieux distincts).
2. Scoring Haversine + mise à jour du score de session.
3. Évaluation des badges (règles métier + Nominatim).

## Contrat API

Source de vérité **live** : Swagger [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).  
Résumé : [api.md](./api.md).

Règle d’or : **ne jamais renvoyer latitude / longitude avant le guess**.
