# Contrat API GetClose

Préfixe `/api`. Auth JWT (`Authorization: Bearer …`) sauf `/health`, `/api/auth/*`, lectures catalogue (`GET /api/categories`, `GET /api/locations`, `GET /api/badges`).

## Auth

- `POST /api/auth/register` `{ pseudo, email, password }` → 201 User
- `POST /api/auth/login` `{ email, password }` → `{ access_token, user }`

## Parties et jeu

- `POST /api/sessions` : crée une partie de 5 manches (lieux tirés au hasard). **Pas de lat/lng dans les rounds.**
- `GET /api/sessions` / `GET /api/sessions/{id}` / `PATCH` / `DELETE`
- `POST /api/guesses` `{ round_id, latitude, longitude }` → distance, score, `actual_location`
- `GET/PATCH/DELETE /api/guesses/{id}`
- `GET /api/rounds` (sans coords avant guess)

## Catalogue

CRUD `/api/categories` et `/api/locations`. Écritures protégées.

## Badges

CRUD `/api/badges` + `POST /api/badges/evaluate` (Nominatim). CRUD `/api/user-badges`.

## Scoring

```
distance_km = Haversine arrondi à 1 décimale
score = max(0, round(5000 * exp(-distance_km / 2000)))
```

Codes : 401 sans token, 403 ressource d’un autre user, 404 inconnu, 409 conflit, 422 validation.
