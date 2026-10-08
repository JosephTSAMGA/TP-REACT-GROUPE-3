# Contribution

Branche d’intégration : **`dev`** (c’est celle à cloner / zipper pour le rendu).

```
main
  └── dev          ← version à rendre
        ├── P1 … P5     (historique de répartition)
        └── feat/integration
```

Lancement et README : racine du dépôt. Détail métier : [docs/CONSIGNES.md](docs/CONSIGNES.md).

| Personne | Front | Back |
|---|---|---|
| P1 | Accueil, routes | User, GameSession, JWT |
| P2 | Carte, manches | — |
| P3 | Résultat, Nominatim UI | Category, Location, tirage |
| P4 | — | Badge, UserBadge |
| P5 | Historique | Round, Guess, scoring |

## Qualité

- Frontend : `npm run lint` / `npm run build` dans `frontend/`
- Backend : `pytest` dans `backend/`
- Pas de secrets dans Git (`.env` ignoré)
- Contrat API : ne pas changer le JSON sans mettre à jour [docs/api.md](docs/api.md)
