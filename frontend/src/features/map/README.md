# Feature `map` — Personne 2

**Outil :** Leaflet + tuiles OpenStreetMap, via `react-leaflet`.  
**Interdit :** carte dessinée à la main, Google Maps, Mapbox.

## MVP (sans backend)

1. Afficher le monde.
2. Clic → `{ latitude, longitude }`.
3. Marker sur le clic.
4. `console.log` des coords.
5. Attribution OSM visible.

Tu ne calcules pas le score. Tu transmets les coords à P1.

## Après le guess

P1 te passe `actualLocation` (`latitude`, `longitude`). Tu ajoutes un **deuxième** marker (point réel).

Packages à installer **quand tu coderas** (pas encore fait) : `leaflet`, `react-leaflet`, et les types Leaflet.
