# GetClose API

Backend FastAPI du jeu de géographie **GetClose** (groupe de 4).

JWT, 8 ressources CRUD, scoring Haversine, badges et géocodage Nominatim.  
Base par défaut : **SQLite** (pas besoin de Docker). PostgreSQL reste optionnel.

## Installation

Docker **n’est pas requis**. Sans `.env`, l’API démarre en SQLite (`getclose.db`).

```bash
cd backend
python -m venv .venv
# Windows : .venv\Scripts\activate
# macOS/Linux : source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

PostgreSQL (optionnel, via Docker) :

```bash
cp .env.example .env
# Décommentez DATABASE_URL postgresql dans .env
docker compose up -d db
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- Santé : http://127.0.0.1:8000/health
- Swagger : http://127.0.0.1:8000/docs

Les tests n’ont pas besoin de PostgreSQL (SQLite temporaire) :

```bash
pytest
```

## Ressources CRUD (8)

| Ressource | Prefix | Relation |
|---|---|---|
| User | `/api/users` + `/api/auth` | un user a plusieurs parties |
| GameSession | `/api/sessions` | une partie appartient à un user |
| Category | `/api/categories` | un thème a plusieurs lieux |
| Location | `/api/locations` | un lieu appartient à une catégorie |
| Round | `/api/rounds` | une manche appartient à une partie |
| Guess | `/api/guesses` | un guess appartient à une manche |
| Badge | `/api/badges` | catalogue de récompenses |
| UserBadge | `/api/user-badges` | un user débloque plusieurs badges |

Les écritures (sauf auth et lectures catalogue) sont protégées par JWT.

`GET /api/rounds` **ne renvoie jamais** les coordonnées du lieu avant le guess.

## Fonctionnalités avancées

1. **Tirage d’une partie** : `POST /api/sessions` choisit 5 lieux distincts et crée les manches.
2. **Scoring** : `POST /api/guesses` calcule Haversine + score `5000 * exp(-d/2000)`.
3. **Badges + Nominatim** : `POST /api/badges/evaluate` (API tierce, mockée dans les tests).

## Structure

```
app/
  main.py
  database.py
  core/          # config, JWT, dépendance auth
  models/        # tables SQLAlchemy
  schemas/       # Pydantic
  routers/       # routes HTTP légères
  services/      # métier (scoring, catalogue, badges, géocodage)
  seed.py
tests/
```
