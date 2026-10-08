# Contrat API GetClose

Préfixe `/api`. Spec interactive : [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

Auth JWT : en-tête `Authorization: Bearer <token>`.  
Routes **publiques** : `/health`, `/api/auth/*`, `GET /api/categories`, `GET /api/locations`, `GET /api/badges`.  
Le reste exige un token (401 sinon). Accès à la ressource d’un autre user → 403.

## Auth

| Méthode | URL | Body | Réponse |
|---|---|---|---|
| POST | `/api/auth/register` | `{ pseudo, email, password }` | 201 User |
| POST | `/api/auth/login` | `{ email, password }` | `{ access_token, user }` |

Pseudo 2–20 caractères, mot de passe ≥ 8. Email déjà pris → 409.

## Users

CRUD via `/api/users` (`GET` liste / `{id}` / `me`, `PATCH /me`, `DELETE /me`). Création = register.

## Parties et jeu

`POST /api/sessions` crée une partie de 5 manches (lieux tirés au hasard).  
Les rounds **ne contiennent pas** `latitude` / `longitude` ni le nom du lieu.

`POST /api/guesses` `{ round_id, latitude, longitude }` → `distance_km`, `score`, `actual_location`.  
Guess déjà soumis → 409. Round inconnu → 404. Lat hors [-90, 90] → 422.

CRUD complet aussi sur `/api/sessions`, `/api/rounds`, `/api/guesses`.

## Catalogue

CRUD `/api/categories` et `/api/locations`. Écritures protégées.  
Un lieu appartient toujours à une catégorie. Suppression d’une catégorie encore peuplée → 409.

## Badges

CRUD `/api/badges`.  
`POST /api/badges/evaluate` (et `POST /api/user-badges`) applique les règles métier et peut appeler Nominatim.

## Scoring

```
distance_km = Haversine, 1 décimale
score = max(0, round(5000 * exp(-distance_km / 2000)))
```

Paris vs Paris → 0 km, score 5000.

## Erreurs HTTP

| Cas | Code |
|---|---|
| Non authentifié | 401 |
| Pas propriétaire | 403 |
| Introuvable | 404 |
| Conflit (doublon, guess déjà fait) | 409 |
| Body / validation | 422 |
