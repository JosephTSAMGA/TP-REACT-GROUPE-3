# Consignes — papier pour tout le monde

Rien à inventer. Pas de carte maison. Pas d’API Google. Pas de Street View.

## Le jeu, en une phrase

Le joueur **voit une photo** → **clique sur le monde** → **valide** → **reçoit un score**.

```
Photo (P4, servie par P3)
        +
Carte Leaflet / OpenStreetMap (P2)
        ↓
clic → { latitude, longitude }
        ↓
POST /api/round/{roundId}/guess  (P3)
        ↓
distance + score + point réel
        ↓
affichage (P1)
```

## Carte = Leaflet + OpenStreetMap

- **Leaflet** affiche la carte et donne lat/lng au clic.
- **OpenStreetMap** fournit les tuiles (le fond de carte).
- **react-leaflet** branche ça dans React.

Personne 2 n’a **aucune** carte à dessiner.

## Photos = fichiers dans le backend

Les images vivent **uniquement** ici :

```
backend/app/data/images/
  paris.jpg
  toulouse.jpg
  tokyo.jpg
  ...
```

Le backend les expose en statique :

```
http://127.0.0.1:8000/static/locations/paris.jpg
```

Le frontend affiche `imageUrl` dans une balise `<img>`. Rien d’autre.

## Contrat API : inchangé

Mêmes champs qu’aujourd’hui. Voir [api.md](./api.md).

**Avant le guess, jamais de latitude / longitude.**  
Ne pas renvoyer `"location": "toulouse"` non plus : ça spoile.

| Quand | JSON |
|---|---|
| `GET /api/round` | `{ roundId, imageUrl, locationId }` |
| `POST /api/round/{id}/guess` | body `{ latitude, longitude }` → `{ distanceKm, score, actualLocation }` |

`imageUrl` est une URL vers **notre** backend, pas vers example.com.

---

## Personne 1 — écran de jeu

Dossier : `frontend/src/features/game`

Tu montes l’écran, tu n’implémentes ni la carte ni l’API.

```
┌─────────────────────────────────────┐
│  Photo (imageUrl)                   │
├─────────────────────────────────────┤
│  Carte Leaflet   (composant P2)     │
│                      📍 clic        │
├─────────────────────────────────────┤
│  Timer    Score    [ GUESS ]        │
└─────────────────────────────────────┘
```

- Timer côté UI seulement.
- Bouton Guess : envoie les coords que P2 t’a données, via `shared/api`.
- Tant que le backend n’est pas prêt : mocks (`VITE_USE_MOCKS=true`).
- 5 manches + score total = **toi** (React). L’API ne gère qu’une manche.

## Personne 2 — carte

Dossier : `frontend/src/features/map`

Packages (quand tu coderas) : `leaflet`, `react-leaflet`, types Leaflet.

Job **minimum** pour le MVP :

1. Afficher le monde (tuiles OSM).
2. Au clic : récupérer `{ latitude, longitude }`.
3. Poser un marker sur le clic.
4. `console.log` des coords — même sans backend, c’est déjà OK.
5. Attribution OSM visible (obligation).

Après le guess (quand P1 te passe `actualLocation`) : un **deuxième** marker pour le point réel.

Tu ne calcules **pas** la distance. Tu ne dessines **pas** de carte.

## Personne 3 — FastAPI

Dossiers : `backend/app/routers`, `backend/app/services`

1. `GET /api/round` et `POST /api/round/{roundId}/guess` selon [api.md](./api.md).
2. Distance Haversine + score (formule dans le contrat).
3. Monter les fichiers statiques : dossier `app/data/images/` → URL `/static/locations/`.
4. `imageUrl` renvoyé = `http://127.0.0.1:8000/static/locations/<fichier>.jpg` (en local).
5. Garder en mémoire `roundId → coords réelles` jusqu’au guess. **Ne pas** envoyer ces coords dans le GET.

CORS : le front est sur `http://127.0.0.1:5173` (déjà prévu dans `main.py`).

## Personne 4 — données

Dossier : `backend/app/data`

1. Remplir `locations.json`.
2. Déposer les `.jpg` dans `backend/app/data/images/`.
3. Chaque ligne JSON pointe vers **une** image, avec des coords **vraies** (le lieu de la photo).

Format d’une ligne (inchangé) :

```json
{
  "id": "1",
  "latitude": 48.8566,
  "longitude": 2.3522,
  "imageUrl": "http://127.0.0.1:8000/static/locations/paris.jpg"
}
```

Pour le MVP : **8 photos** suffisent (5 manches + un peu de relance).  
Photos libres (Wikimedia, Unsplash) ou photos du groupe. **Pas** de Street View Google.

Le nom du fichier (`paris.jpg`) n’est **jamais** renvoyé comme indice dans `GET /round` — seulement `imageUrl` + `locationId`.

Détail : [backend/app/data/README.md](../backend/app/data/README.md).

## Personne 5 — qualité

- Tests scoring : Paris/Paris → 0 km, score 5000.
- Tests API : GET 200 **sans** lat/lng ; POST sans latitude → 422 ; round inconnu → 404.
- Vérifier que `imageUrl` charge bien (fichier existant).
- Plus tard : E2E START → clic carte → GUESS → résultat.

---

## Interdit

- Dessiner une carte / canvas / SVG monde maison
- Google Maps, Mapbox, Street View
- Renvoyer lat/lng (ou le nom de la ville) **avant** le guess
- Mettre les images dans `frontend/public` — elles restent **backend**
