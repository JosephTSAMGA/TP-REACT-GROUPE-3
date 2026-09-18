# Consignes groupe

Une app. Un contrat API. **Cinq personnes, front + back.**

```
Photo → carte Leaflet → clic {latitude, longitude} → POST /guess → score
```

Détail API : [api.md](./api.md)  
Git : [CONTRIBUTING.md](../CONTRIBUTING.md)

---

## Git (tout le monde)

```
git fetch
git checkout P1    # ou P2 P3 P4 P5 — TA branche
```

On merge vers `dev`, puis `dev` → `main`.  
Tu as besoin d’une branche en plus ? Tu la crées depuis la tienne.

**Pas de zip sur GitHub.** Pas de commit sur `main` direct.

---

## Contrat (personne n’y touche sans le groupe)

- `GET /api/round` → `{ roundId, imageUrl, locationId }` — **jamais** lat/lng ni nom de ville
- `POST /api/round/{roundId}/guess` `{ latitude, longitude }` → `{ distanceKm, score, actualLocation }`
- Photos : `http://127.0.0.1:8000/static/locations/paris.jpg`
- 5 manches = 5× `GET /api/round` **côté React**

---

## Qui fait quoi

### P1
**Front** `frontend/src/features/game` : start, timer, 5 manches, score, bouton Guess. Tu **importes** la carte P2, tu ne la recodes pas.  
**Back** `backend/app/schemas.py` : modèles Pydantic = le JSON du contrat.

Déjà fait : écran start, timer, squelette GameScreen (TODOs encore).  
À faire : charger le round, photo, Guess, next, restart + `schemas.py`.

### P2
**Front** `frontend/src/features/map` : Leaflet + OSM, clic → coords, marker.  
**Back** `backend/app/services/scoring.py` : Haversine + `score = max(0, round(5000 * exp(-km / 2000)))`.

Déjà fait : carte + clic + marker (sur `P2`).  
À faire : brancher la carte **dans** GameScreen (pas un 2ᵉ `main.tsx`), 2ᵉ marker après guess, coder `scoring.py`.

### P3
**Front** `frontend/src/shared/api` : `getRound` / `postGuess` (vrai HTTP quand l’API existe).  
**Back** `routers/rounds.py` + `services/game.py` : les 2 routes + mémoire `roundId → coords`. Monter `/static/locations/`.

Déjà fait : client + mocks (Phase 0). Router vide.  
À faire : implémenter les routes **sans** renvoyer lat/lng dans le GET.

### P4
**Front** : `<img src={imageUrl} />` dans l’écran de jeu (avec P1).  
**Back** `backend/app/data/` : `locations.json` + **8 jpg** dans `images/`.

Déjà fait : 1 ligne Paris, **0 image**.  
À faire : 8 photos libres + JSON avec les **vraies** coords.

### P5
**Front** `app/` : coller GameScreen + carte P2, mocks, CI front.  
**Back** `backend/tests/` : tests scoring, API, « pas de coords dans le GET ».

Déjà fait : `/health`, CI, contrat, architecture.  
À faire : tests dès que P2/P3 livrent + intégration P1↔P2.

---

## Interdit

- Carte maison / Google Maps / Mapbox / Street View
- Images dans `frontend/public`
- Lat/lng (ou le nom de la ville) **avant** le guess
- Recoder le dossier de quelqu’un d’autre
