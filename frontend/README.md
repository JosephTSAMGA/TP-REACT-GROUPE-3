# Frontend

```bash
npm install
npm run dev
```

Ouvre [http://127.0.0.1:5173](http://127.0.0.1:5173).  
Le backend doit tourner sur [http://127.0.0.1:8000](http://127.0.0.1:8000) (voir le README à la racine du repo).

Arborescence : `src/app`, `src/features/{game,map,result,history}`, `src/shared`.

Le jeu appelle l’API réelle (`/api/auth`, `/api/sessions`, `/api/guesses`).  
Carte = Leaflet + OpenStreetMap (`react-leaflet`).
