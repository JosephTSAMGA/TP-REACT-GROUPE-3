# Feature `game`

- **P1** — `StartScreen` (inscription / connexion JWT)
- **P2** — `GamePage`, `RoundScreen` (manche, timer, confirmer)

`GamePage` envoie le clic à `POST /api/guesses`. Il ne calcule plus le score localement.
