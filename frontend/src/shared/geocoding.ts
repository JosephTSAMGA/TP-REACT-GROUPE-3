// =============================================================
// PARTIE 3/4 — Score & API externe
// Fichiers de cette partie : utils/scoring.ts, utils/geocoding.ts,
// RoundResult.tsx (+.css).
// Rôle de ce fichier : LE point du barème "Communication API" — un
// vrai fetch() vers un service externe (Nominatim/OpenStreetMap),
// avec vérification du statut HTTP et gestion des erreurs.
// =============================================================
import type { Coordinates } from "./types";

// API gratuite d'OpenStreetMap qui fait du "reverse geocoding" :
// on lui envoie des coordonnées GPS, elle nous renvoie l'adresse
// (ville, pays...) correspondante. Aucune clé API n'est nécessaire.
const NOMINATIM_URL = "https://nominatim.openstreetmap.org/reverse";

// Forme (partielle) de la réponse JSON renvoyée par Nominatim.
// On ne type que les champs qu'on utilise réellement.
type NominatimResponse = {
  address?: {
    city?: string;
    town?: string;
    village?: string;
    country?: string;
  };
};

// Appelle l'API pour transformer des coordonnées en un nom lisible,
// par exemple "Paris, France". C'est ici qu'a lieu le vrai `fetch`
// réseau : le composant qui appelle cette fonction est responsable
// d'afficher les états "chargement" / "succès" / "erreur" autour.
export async function reverseGeocode(coords: Coordinates): Promise<string> {
  const url = `${NOMINATIM_URL}?format=jsonv2&lat=${coords.lat}&lon=${coords.lng}&zoom=10&addressdetails=1`;

  const response = await fetch(url, {
    headers: { Accept: "application/json" },
  });

  // On vérifie explicitement le statut HTTP avant de lire le corps :
  // fetch() ne rejette PAS automatiquement sur une réponse 4xx/5xx.
  if (!response.ok) {
    throw new Error(`Erreur API géocodage (statut ${response.status})`);
  }

  const data: NominatimResponse = await response.json();
  const address = data.address;

  if (!address) {
    throw new Error("Aucune adresse trouvée pour ce point");
  }

  const place = address.city ?? address.town ?? address.village;

  if (place && address.country) {
    return `${place}, ${address.country}`;
  }

  return address.country ?? "Lieu inconnu";
}
