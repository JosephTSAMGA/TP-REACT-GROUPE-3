# Contribution

## Branches

```
main          ← stable (pas de commit direct)
  └── dev     ← intégration
        ├── P1
        ├── P2
        ├── P3
        ├── P4
        └── P5
```

`git fetch && git checkout P2` (ta lettre).  
Branche en plus : depuis la tienne, puis merge vers `dev`.

| Branche | Front | Back |
|---|---|---|
| `P1` | `features/game` | `app/schemas.py` |
| `P2` | `features/map` | `app/services/scoring.py` |
| `P3` | `shared/api` | `routers/rounds.py` + `services/game.py` + static |
| `P4` | photo (`<img>`) | `app/data/` (json + images) |
| `P5` | `app/` + CI front | `tests/` + CI back |

Papier : `docs/CONSIGNES.md`. Contrat : `docs/api.md`.

Ne pas changer le JSON sans `docs/api.md` + `docs/openapi.yaml` dans la même PR.

Interdit : carte maison, Google Maps, images dans le frontend, lat/lng avant le guess, zip sur le repo.
