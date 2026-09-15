# Données — Personne 4

Les photos restent **dans le backend**. Pas dans `frontend/public`.

```
backend/app/data/
  locations.json
  images/              ← déposer les jpg ici
    paris.jpg
    toulouse.jpg
    tokyo.jpg
```

Personne 3 expose ce dossier en :

`http://127.0.0.1:8000/static/locations/<fichier>.jpg`

## `locations.json`

Une ligne = une photo + les **vraies** coordonnées du lieu (jamais envoyées au front avant le guess).

```json
{
  "id": "1",
  "latitude": 48.8566,
  "longitude": 2.3522,
  "imageUrl": "http://127.0.0.1:8000/static/locations/paris.jpg"
}
```

Champs inchangés par rapport au contrat.

## Consignes simples

- MVP : **8 images** suffisent.
- Photo reconnaissable, coords du monument / lieu (pas « un peu la ville »).
- Licence libre (Wikimedia, Unsplash) ou photos du groupe.
- Pas de Google Street View.
- Le nom de fichier ne doit pas apparaître comme indice dans `GET /api/round`.
