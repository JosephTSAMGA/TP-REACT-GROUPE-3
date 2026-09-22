// =============================================================
// PARTIE 3/4 — Score & API externe
// Fichiers de cette partie : utils/scoring.ts, utils/geocoding.ts,
// RoundResult.tsx (+.css).
// Rôle de ce fichier : transformer deux positions GPS en une distance,
// puis cette distance en points. Pas de React ici, que des fonctions
// pures (même entrée → toujours la même sortie), donc facile à tester
// et à expliquer indépendamment du reste de l'appli.
// =============================================================
import type { Coordinates } from "./types";

// Rayon moyen de la Terre en kilomètres, utilisé par la formule de Haversine.
const EARTH_RADIUS_KM = 6371;

// La moitié de la circonférence de la Terre (~20015 km) : la distance
// maximale possible entre deux points GPS (des antipodes parfaits).
// On s'en sert comme référence pour transformer une distance en score.
const MAX_DISTANCE_KM = 20015;

// Le score maximum qu'on peut gagner sur une seule manche.
const MAX_POINTS_PER_ROUND = 1000;

// Convertit des degrés en radians (nécessaire pour Math.sin / Math.cos).
function toRadians(degrees: number): number {
  return (degrees * Math.PI) / 180;
}

// Formule de Haversine : calcule la distance "à vol d'oiseau" en kilomètres
// entre deux points GPS, en tenant compte de la courbure de la Terre.
// C'est la formule standard utilisée par les jeux type GeoGuessr.
export function haversineDistanceKm(a: Coordinates, b: Coordinates): number {
  const dLat = toRadians(b.lat - a.lat);
  const dLng = toRadians(b.lng - a.lng);

  const lat1 = toRadians(a.lat);
  const lat2 = toRadians(b.lat);

  const h =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(lat1) * Math.cos(lat2) * Math.sin(dLng / 2) ** 2;

  const c = 2 * Math.atan2(Math.sqrt(h), Math.sqrt(1 - h));

  return EARTH_RADIUS_KM * c;
}

// Transforme une distance en points : plus le joueur est proche du vrai
// lieu, plus il gagne de points. À 0 km, il gagne le maximum (1000 pts).
// À l'autre bout de la Terre (~20015 km), il gagne 0 point.
// La relation est linéaire, ce qui la rend simple à expliquer à l'oral.
export function computeScore(distanceKm: number): number {
  const ratio = Math.max(0, 1 - distanceKm / MAX_DISTANCE_KM);
  return Math.round(ratio * MAX_POINTS_PER_ROUND);
}
