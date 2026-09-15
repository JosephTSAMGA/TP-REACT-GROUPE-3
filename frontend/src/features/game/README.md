# Feature `game` — Personne 1

Écran de manche : **photo** + **carte P2** + timer + score + bouton Guess.

```
Photo (imageUrl du GET /round)
Carte (composant features/map)
Timer | Score | [ GUESS ]
```

- Timer **UI seulement** (pas d’expire côté API).
- Guess envoie les lat/lng fournis par P2, via `shared/api`.
- Mocks tant que `VITE_USE_MOCKS` n’est pas `false`.
- 5 manches et score total = React, pas l’API.

Tu n’implémentes ni Leaflet ni le scoring.
