# Contrat API

Source machine : [openapi.yaml](./openapi.yaml).  
Toute évolution du JSON passe par une PR qui met à jour ce contrat **avant** le code.

Préfixe : `/api`.  
Timer : **côté UI uniquement** (le serveur n’expire pas les manches en Phase 1–3).

## Décisions figées

| Question | Décision |
|---|---|
| Préfixe | `/api` |
| `locationId` dans `GET /round` | Oui (string), **sans** lat/lng |
| Lat/lng avant guess | Interdit |
| Lat/lng après guess | Oui, dans `actualLocation` (pour afficher le point réel) |
| Round inconnu | `404` |
| Body invalide | `422` |
| Guess déjà soumis | `409` |
| 5 manches | Le frontend appelle `GET /api/round` 5 fois |
| Photos | Fichiers backend, URL `/static/locations/<fichier>.jpg` |
| Carte | Hors API : Leaflet + OSM côté React |

## `GET /api/round`

Crée une manche et renvoie l’image à localiser. Les coordonnées réelles restent côté serveur.

Réponse `200` :

```json
{
  "roundId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "imageUrl": "http://127.0.0.1:8000/static/locations/paris.jpg",
  "locationId": "1"
}
```

Champs **absents** : `latitude`, `longitude`, nom de ville.

`imageUrl` est l’URL d’un fichier servi par **ce** backend (`/static/locations/...`). Même forme JSON qu’avant : c’est toujours une URI. En local : `http://127.0.0.1:8000/static/locations/<fichier>.jpg`.

Fichiers physiques : `backend/app/data/images/`. Montage statique : Personne 3. Contenu : Personne 4.

## `POST /api/round/{roundId}/guess`

Body :

```json
{
  "latitude": 43.6045,
  "longitude": 1.444
}
```

Contraintes : `latitude` ∈ [-90, 90], `longitude` ∈ [-180, 180].

Réponse `200` :

```json
{
  "distanceKm": 12.4,
  "score": 4969,
  "actualLocation": {
    "locationId": "1",
    "latitude": 48.8566,
    "longitude": 2.3522
  }
}
```

`actualLocation` n’existe **qu’après** un guess valide. Il permet à la carte d’afficher le point réel.

## Erreurs

| Cas | Statut | Corps |
|---|---|---|
| `roundId` inconnu | `404` | `{ "detail": "Round not found" }` |
| Guess déjà soumis pour ce round | `409` | `{ "detail": "Guess already submitted" }` |
| Body manquant / types invalides / lat hors bornes | `422` | erreur de validation FastAPI |

## Scoring (spécification pour P3 / tests P5)

- Distance : Haversine, en kilomètres, arrondie à **1 décimale**.
- Score entier, plage **0–5000** :

```
score = max(0, round(5000 * exp(-distanceKm / 2000)))
```

Exemples attendus par les tests unitaires :

- distance `0` → score `5000`
- Paris vs Paris → distance `0`
- une grande distance produit un score **strictement inférieur** à une petite distance

## État serveur

- Un `roundId` est un UUID.
- Le process FastAPI garde en mémoire `roundId → { locationId, latitude, longitude, guessed }`.
- Redémarrage du serveur → les rounds en cours deviennent `404`. Acceptable pour le MVP.
- Pas d’endpoint `POST /games` en Phase 1–3. Le tirage d’une partie est `POST /api/sessions/random` (voir plus bas).

## Lieux, catégories et partie aléatoire

Ressources de l’étudiant B. Le score reste calculé dans le navigateur : une session renvoie donc les coordonnées, comme les manches déjà codées en dur dans le front. Ça ne change pas `GET /api/round`, qui continue de cacher lat/lng.

Une **Location** appartient à une **Category** (`categoryId` obligatoire).

| Méthode | Chemin | Rôle |
|---|---|---|
| `GET` | `/api/categories` | Liste des thèmes (`locationCount` inclus) |
| `POST` | `/api/categories` | Créer un thème `{ "name": "Océans" }` (slug généré si absent) |
| `GET` | `/api/categories/{id}` | Thème + ses lieux |
| `PUT` | `/api/categories/{id}` | Remplacer le thème |
| `DELETE` | `/api/categories/{id}` | Supprimer. `409` si des lieux y sont encore rattachés |
| `GET` | `/api/locations?categoryId=` | Liste des lieux (filtre optionnel) |
| `POST` | `/api/locations` | Créer un lieu |
| `GET` | `/api/locations/{id}` | Un lieu, avec sa catégorie |
| `PUT` | `/api/locations/{id}` | Remplacer un lieu |
| `DELETE` | `/api/locations/{id}` | Supprimer un lieu |
| `POST` | `/api/sessions/random` | Tirer des lieux au hasard et ouvrir une partie |
| `GET` | `/api/sessions/{id}` | Relire la même partie |

`POST /api/sessions/random` :

```json
{ "size": 5, "categoryId": 1 }
```

`size` vaut 5 par défaut (1 à 20). `categoryId` est optionnel : sans lui, le tirage porte sur tous les lieux. La réponse `201` contient les lieux dans l’ordre du tirage. S’il n’y en a pas assez, `422`. Catégorie inconnue : `404`.

Au premier démarrage, la base SQLite (`backend/app/data/geoguessr.db`) est créée et remplie avec trois thèmes : Monuments, Capitales, Sites naturels. Chaque thème a au moins 5 lieux, pour qu’une partie puisse démarrer dans n’importe lequel.
