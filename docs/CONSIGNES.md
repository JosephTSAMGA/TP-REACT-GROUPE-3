# Consignes — GetClose (groupe de 4)

Jeu de géographie : une photo, une carte, 5 manches.  
Front React (`frontend/`) + API FastAPI (`backend/`).

Lancement : voir le [README racine](../README.md). **Docker n’est pas obligatoire** (SQLite par défaut).

## Flux

```
Inscription / connexion (JWT)
        ↓
POST /api/sessions          → 5 manches tirées au hasard (sans lat/lng)
        ↓
Photo + carte Leaflet
        ↓
POST /api/guesses           → distance Haversine + score + lieu réel
        ↓
Écran résultat (Nominatim pour le lieu cliqué)
        ↓
Après 5 manches → score final + historique
```

## Répartition

| Personne | Front | Back |
|---|---|---|
| P1 | Accueil, routes, NavBar, `StartScreen` | User, GameSession, JWT |
| P2 | `GamePage`, `RoundScreen`, carte Leaflet | consomme Round / Guess |
| P3 | `RoundResult`, Nominatim (affichage) | Category, Location, tirage de partie |
| P4 | — | Badge, UserBadge, géocodage serveur |
| P5 | Historique, écran de fin | Round, Guess, scoring Haversine |

## Routes front

| URL | Écran |
|---|---|
| `/` | Accueil : inscription ou connexion |
| `/jeu` | Manche (photo + carte + Valider) |
| (état interne) | Résultat de manche |
| `/resultats` | Score final |
| `/historique` | Parties du joueur (API `/api/sessions`) |

## Règles

- Jamais de lat/lng (ni le nom du lieu) **avant** le guess.
- Carte = Leaflet + OpenStreetMap, pas de carte maison, pas de Google Maps.
- Score calculé **côté API** (`POST /api/guesses`).
- Contrat détaillé : [api.md](./api.md) · spec live : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## Git

Travail intégré sur `dev`. Branches `P1`…`P5` = historique de répartition.
