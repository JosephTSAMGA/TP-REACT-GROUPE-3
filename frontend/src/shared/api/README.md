# Client API

`registerUser` / `loginUser` (JWT), `createSession`, `postGuess`, `listSessions`.

Le token est stocké dans `localStorage` (`getclose_token`).
Les manches renvoyées par `GET/POST /api/sessions` n’incluent **pas** les coordonnées du lieu.
