# Contribution

## Branches

`main` est protégée. Tout passe par une pull request.

| Branche | Qui | Contenu |
|---|---|---|
| `feat/p1-game-ui` | Personne 1 | Écran de jeu, timer, score, transitions |
| `feat/p2-map` | Personne 2 | Leaflet + OSM, marker, lat/lng |
| `feat/p3-api` | Personne 3 | Endpoints, scoring, fichiers statiques `/static/locations/` |
| `feat/p4-locations` | Personne 4 | `locations.json` + images dans `app/data/images/` |
| `feat/p5-ci-tests` | Personne 5 | Tests, CI, mocks, bugs d’intégration |

Nommage : `feat/<id>-<sujet>`, `fix/<id>-<sujet>`, `docs/<sujet>`.

## Contrat API

Ne pas changer le JSON sans mettre à jour `docs/openapi.yaml` et `docs/api.md` dans la même PR.

Papier groupe (Leaflet, photos, qui fait quoi) : `docs/CONSIGNES.md`.  
Interdit : carte maison, Google Maps, images dans le frontend, lat/lng avant le guess.

## Qualité

- Frontend : ESLint + Prettier (`npm run lint` / `npm run format` dans `frontend/`)
- Backend : Ruff (`ruff check` dans `backend/`)
- CI GitHub Actions sur chaque PR
