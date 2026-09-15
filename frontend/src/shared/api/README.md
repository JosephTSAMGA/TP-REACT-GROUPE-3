# Client API partagé

Types + mocks + `getRound` / `postGuess`.

Les mocks sont actifs tant que `VITE_USE_MOCKS` n’est pas `false` (voir `.env.example`).
Les coordonnées réelles n’existent que dans `GuessResponse.actualLocation`.

`imageUrl` pointe vers le backend : `http://127.0.0.1:8000/static/locations/<fichier>.jpg`.
Le contrat JSON ne change pas.
