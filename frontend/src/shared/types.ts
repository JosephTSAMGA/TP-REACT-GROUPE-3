// =============================================================
// FICHIER PARTAGÉ — utilisé par les 4 parties du projet.
// Chacun doit au moins jeter un œil ici : ce sont les "contrats" de
// données utilisés partout (une position GPS, une manche, un résultat).
// =============================================================
// Types partagés entre plusieurs composants du jeu.
// On les centralise ici pour éviter de retaper le même type
// (Coordinates) dans App.tsx, RoundScreen.tsx et InteractiveMap.tsx.

// Une position GPS : latitude / longitude.
export type Coordinates = {
  lat: number;
  lng: number;
};

// Une manche du jeu : l'image à afficher + la vraie position
// (la "correction") + un nom lisible pour l'écran de résultat.
export type Round = {
  imageUrl: string;
  answer: Coordinates;
  label: string;
};

// Le résultat d'une manche une fois que le joueur a confirmé sa réponse.
export type RoundOutcome = {
  guess: Coordinates;
  answer: Round;
  distanceKm: number;
  points: number;
};
