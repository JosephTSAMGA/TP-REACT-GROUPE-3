// =============================================================
// PARTIE 3/4 — Score & API externe
// Fichiers de cette partie : utils/scoring.ts, utils/geocoding.ts,
// RoundResult.tsx (+.css).
// Rôle de ce fichier : l'écran affiché après chaque manche. C'est ici
// que le fetch de geocoding.ts est réellement déclenché (dans un
// useEffect) et que ses 3 états (chargement/succès/erreur) sont
// traduits en affichage à l'écran.
// =============================================================
import { useEffect, useState } from "react";
import "./RoundResult.css";
import { reverseGeocode } from "../../shared/geocoding";
import type { RoundOutcome } from "../../shared/types";

type RoundResultProps = {
  outcome: RoundOutcome;
  cumulativeScore: number;
  isLastRound: boolean;
  onContinue: () => void;
};

export default function RoundResult({
  outcome,
  cumulativeScore,
  isLastRound,
  onContinue,
}: RoundResultProps) {
  // Trois états possibles pour l'appel API, affichés différemment à l'écran :
  // - loading: la requête est en cours (on affiche un message d'attente)
  // - le nom du lieu une fois la requête réussie
  // - error: la requête a échoué (on affiche un message d'erreur, le jeu
  //   continue quand même à fonctionner sans ce nom)
  const [placeName, setPlaceName] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // `cancelled` évite de mettre à jour le state si le composant est
    // démonté avant la fin de la requête (ex: le joueur clique très vite
    // sur "manche suivante").
    let cancelled = false;

    reverseGeocode(outcome.guess)
      .then((name) => {
        if (!cancelled) setPlaceName(name);
      })
      .catch(() => {
        if (!cancelled) setError("Impossible de récupérer le nom du lieu.");
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });

    return () => {
      cancelled = true;
    };
  }, [outcome.guess]);

  return (
    <div className="round-result">
      <div className="round-result-card">
        <h2 className="round-result-title">{outcome.answer.label}</h2>

        <p className="round-result-distance">
          Distance : <strong>{outcome.distanceKm.toFixed(1)} km</strong>
        </p>

        <p className="round-result-guess-place">
          {loading && "Recherche du lieu pointé…"}
          {!loading && error && error}
          {!loading && !error && placeName && <>Tu as pointé : <strong>{placeName}</strong></>}
        </p>

        <p className="round-result-points">+{outcome.points} pts</p>
        <p className="round-result-cumulative">
          Score total : {cumulativeScore.toLocaleString("fr-FR")} pts
        </p>

        <button className="round-result-button" onClick={onContinue}>
          {isLastRound ? "Voir mes résultats" : "Manche suivante"}
        </button>
      </div>
    </div>
  );
}
