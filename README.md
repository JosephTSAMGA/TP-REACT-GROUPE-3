# GetClose

**Jeu de géographie web inspiré de GeoGuessr** : une photo d'un lieu réel s'affiche, le joueur clique sur la carte là où il pense qu'elle a été prise, et marque des points selon la distance. Une partie = 5 manches.

Projet de groupe (4 étudiants) réalisé en septembre 2026 dans le cadre d'un TP React + FastAPI.

![Statut](https://img.shields.io/badge/statut-termin%C3%A9-success) ![Tests](https://img.shields.io/badge/tests%20API-41%20passent-success)

---

## Fonctionnalités

- **Comptes joueurs** : inscription et connexion avec authentification JWT
- **Partie de 5 manches** tirées au hasard parmi des lieux classés par catégories
- **Carte interactive** Leaflet + OpenStreetMap pour placer sa réponse
- **Score calculé côté serveur** à partir de la distance (formule de Haversine)
- **Écran de résultat** par manche, avec le nom du lieu cliqué (géocodage inverse via l'API Nominatim)
- **Historique** des parties du joueur
- **Badges** débloqués selon des règles métier : première partie, nombre de parties, score élevé, exploration de plusieurs pays

## Stack technique

| Couche | Technologies |
|---|---|
| Frontend | React 19, TypeScript, Vite, React Router, Leaflet / react-leaflet |
| Backend | FastAPI, SQLAlchemy 2, Pydantic v2 |
| Base de données | SQLite par défaut, PostgreSQL en option (Docker Compose) |
| Authentification | JWT (python-jose), mots de passe hachés avec bcrypt (passlib) |
| API tierce | Nominatim (OpenStreetMap) pour le géocodage inverse |
| Qualité | pytest, Ruff, ESLint, Prettier, intégration continue GitHub Actions |

## Architecture

Monorepo `frontend/` + `backend/`. Côté API, le code suit une séparation **routers → services → models** : les routes restent minces, la logique métier est dans les services.

**8 ressources CRUD** : User, GameSession, Category, Location, Round, Guess, Badge, UserBadge.

```
Inscription / connexion (JWT)
        ↓
POST /api/sessions   → 5 manches tirées au hasard (sans coordonnées)
        ↓
Photo + clic sur la carte
        ↓
POST /api/guesses    → distance + score calculés par l'API, lieu réel révélé
        ↓
Résultat de manche → après 5 manches : score final + historique
```

Détails : [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) · Contrat d'API : [docs/api.md](docs/api.md)

## Sécurité

Quelques choix de conception orientés sécurité :

- **Mots de passe** jamais stockés en clair : hachage bcrypt, algorithme volontairement lent contre la force brute
- **Jetons JWT signés** avec date d'expiration, vérifiés sur chaque route protégée
- **Secrets hors du code** : clé JWT et URL de base lues depuis un fichier `.env` non versionné
- **Anti-triche** : les coordonnées d'un lieu ne sont jamais envoyées au client avant sa réponse, et le score est calculé uniquement côté serveur
- **CORS** restreint aux origines du frontend en développement

## Lancer le projet

Prérequis : **Node.js 20+** et **Python 3.9+** (3.12 recommandé). Docker n'est pas obligatoire.

Il faut deux terminaux : un pour le backend, un pour le frontend.

### 1. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- Santé : http://127.0.0.1:8000/health
- Documentation interactive (Swagger) : http://127.0.0.1:8000/docs

<details>
<summary>Option : PostgreSQL avec Docker</summary>

```bash
cd backend
cp .env.example .env             # Windows : copy .env.example .env
```

Dans `.env`, commentez la ligne SQLite et décommentez :

```
DATABASE_URL=postgresql+psycopg://getclose:getclose@localhost:5432/getclose
```

Puis :

```bash
docker compose up -d db
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

</details>

### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

Ouvrir http://127.0.0.1:5173 (Vite redirige `/api` vers le backend sur le port 8000).
Sur l'accueil, créer un compte (pseudo, email, mot de passe d'au moins 8 caractères) puis **Créer un compte et jouer**.

### Tests

```bash
cd backend
pytest
```

## Répartition du travail

| Rôle | Front | Back |
|---|---|---|
| P1 | Accueil, routes, NavBar, `StartScreen` | User, GameSession, JWT |
| P2 | `GamePage`, `RoundScreen`, carte Leaflet | Consomme Round / Guess |
| P3 | `RoundResult`, affichage Nominatim | Category, Location, tirage de partie |
| P4 | — | Badge, UserBadge, géocodage serveur |
| P5 | Historique, écran de fin | Round, Guess, scoring Haversine |

Contributeurs : [@JosephTSAMGA](https://github.com/JosephTSAMGA), [@Alexestgrand](https://github.com/Alexestgrand), [@azizz12](https://github.com/azizz12), cagaetan.

## Documentation

- [docs/CONSIGNES.md](docs/CONSIGNES.md) : règles du jeu, flux et répartition
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) : stack, dossiers, ressources et relations
- [docs/api.md](docs/api.md) : contrat HTTP
- [CONTRIBUTING.md](CONTRIBUTING.md) : organisation des branches
