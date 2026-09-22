# Consignes groupe

P4 est hors projet. **4 personnes.** Une seule app : `frontend/` (plus de `getclose-ts/`).

```
cd frontend && npm install && npm run dev
```

## Qui possède quoi

| Qui | Fichiers |
|---|---|
| **P1** | `src/app/` (routes, NavBar), `features/game/StartScreen.*` |
| **P2** | `features/game/GamePage.tsx`, `RoundScreen.*`, `features/map/InteractiveMap.tsx` |
| **P3** | `shared/scoring.ts`, `shared/geocoding.ts`, `features/result/RoundResult.*` |
| **P5** | `shared/storage.ts`, `features/history/FinishedScreen.*`, `HistoryScreen.*` |

`shared/types.ts` = contrat commun (coords, manche).

## Routes

- `/` accueil + formulaire pseudo (P1)
- `/jeu` 5 manches + carte (P2)
- après chaque manche → RoundResult (P3) + Nominatim
- `/resultats` fin de partie (P5)
- `/historique` localStorage (P5)

## Git

`git checkout P1` (ou P2 / P3 / P5). Merge vers `dev`. Pas de P4.
