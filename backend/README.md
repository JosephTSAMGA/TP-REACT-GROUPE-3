# Backend

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

`GET /health` répond. Lieux et catégories :

- `GET` / `POST /api/categories`, `GET` / `PUT` / `DELETE /api/categories/{id}`
- `GET` / `POST /api/locations`, `GET` / `PUT` / `DELETE /api/locations/{id}`
- `POST /api/sessions/random` tire 5 lieux au hasard (filtre `categoryId` possible)
- `GET /api/sessions/{id}` relit cette partie

La base SQLite est créée au premier lancement (`app/data/geoguessr.db`) et remplie si elle est vide. Une location appartient toujours à une category.

Routes de manche (`/api/round`) : P3. Scoring : P2. Voir `docs/api.md`.
