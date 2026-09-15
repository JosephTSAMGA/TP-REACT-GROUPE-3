# Contribution

## Branches

```
main          ← version stable
  └── dev     ← intégration
        ├── P1
        ├── P2
        ├── P3
        ├── P4
        └── P5
```

Chacun travaille sur **sa** branche (`P1` … `P5`).  
Besoin d’une branche en plus ? Ils la créent depuis la leur (`feat/…`, `fix/…`).  
On merge vers `dev`, puis `dev` → `main`.

| Branche | Qui |
|---|---|
| `P1` | Personne 1 — écran de jeu, timer, score |
| `P2` | Personne 2 — Leaflet + OSM |
| `P3` | Personne 3 — FastAPI, scoring, `/static/locations/` |
| `P4` | Personne 4 — `locations.json` + images |
| `P5` | Personne 5 — tests, CI, intégration |

Démarrage : `git fetch && git checkout P2` (par exemple).

## Contrat API

Ne pas changer le JSON sans mettre à jour `docs/openapi.yaml` et `docs/api.md` dans la même PR.

Papier groupe : `docs/CONSIGNES.md`.  
Interdit : carte maison, Google Maps, images dans le frontend, lat/lng avant le guess.

## Qualité

- Frontend : ESLint + Prettier (`npm run lint` / `npm run format` dans `frontend/`)
- Backend : Ruff (`ruff check` dans `backend/`)
- CI GitHub Actions sur chaque PR
