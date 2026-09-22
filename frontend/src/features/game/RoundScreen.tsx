// =============================================================
// PARTIE 2/4 — Le cœur du jeu (carte & manches)
// Fichiers de cette partie : GamePage.tsx, RoundScreen.tsx (+.css),
// InteractiveMap.tsx.
// Rôle de ce fichier : afficher UNE manche (photo + carte + timer +
// bouton confirmer). Ce composant ne connaît PAS le vrai lieu à
// deviner : il se contente de renvoyer la position cliquée par le
// joueur à son parent (GamePage) via `onConfirm`. C'est GamePage qui
// fera la comparaison avec la bonne réponse.
// =============================================================
import { useState, useEffect } from "react";
import "./RoundScreen.css";
import InteractiveMap from "../map/InteractiveMap";
import type { Coordinates } from "../../shared/types";

type RoundScreenProps = {
  imageUrl: string;
  roundNumber: number;
  totalRounds: number;
  cumulativeScore: number;
  timerSeconds?: number;
  onTimeUp?: () => void;
  // Callback déclenché quand le joueur clique sur "Confirmer".
  // On remonte juste les coordonnées choisies, pas de calcul ici.
  onConfirm: (guess: Coordinates) => void;
};

export default function RoundScreen({
  imageUrl,
  roundNumber,
  totalRounds,
  cumulativeScore,
  timerSeconds = 60,
  onTimeUp = () => {},
  onConfirm,
}: RoundScreenProps) {
  // Hook n°1 : useState pour le temps restant (affiché et décrémenté
  // chaque seconde par le useEffect ci-dessous).
  const [timeLeft, setTimeLeft] = useState<number>(timerSeconds);

  // Hook n°2 : useState pour la position choisie par le joueur sur la
  // carte. `null` tant qu'il n'a encore rien cliqué : ça sert à la fois
  // à afficher un texte différent sur le bouton et à le désactiver.
  const [guess, setGuess] = useState<Coordinates | null>(null);

  // Hook n°3 : useEffect qui fait fonctionner le chronomètre.
  // Comme timeLeft est dans le tableau de dépendances, cet effet est
  // relancé à CHAQUE seconde (dès que timeLeft change) : on programme
  // un nouveau setInterval d'1 seconde à chaque fois.
  useEffect(() => {
    if (timeLeft <= 0) {
      onTimeUp();
      return;
    }
    const interval = setInterval(() => {
      setTimeLeft((prev) => prev - 1);
    }, 1000);

    // Fonction de nettoyage : React l'appelle avant de relancer l'effet
    // (ou quand le composant est démonté). Sans elle, on empilerait des
    // dizaines de timers en parallèle → bug classique avec setInterval.
    return () => clearInterval(interval);
  }, [timeLeft, onTimeUp]);

  const handleConfirmClick = () => {
    if (guess) {
      onConfirm(guess);
    }
  };

  return (
    <div className="round-screen">
      <header className="round-header">
        <span className="round-count">Manche {roundNumber} / {totalRounds}</span>
        <div className="round-timer-block">
          {/* data-low bascule la couleur en rouge via le CSS quand il reste peu de temps. */}
          <span className="round-timer" data-low={timeLeft <= 10}>{timeLeft}s</span>
          <span className="round-go">Go go go !</span>
        </div>
        <span className="round-cumulative">{cumulativeScore.toLocaleString("fr-FR")} pts</span>
      </header>

      <div className="round-play-area">
        <div className="round-map-space">
          {/* On passe directement setGuess : à chaque clic sur la carte,
              InteractiveMap nous renvoie les coordonnées et on les stocke. */}
          <InteractiveMap onPositionChange={setGuess} />
        </div>
        <img className="round-image" src={imageUrl} alt="Lieu à deviner" />
      </div>

      <button
        className="round-confirm-button"
        disabled={!guess}
        onClick={handleConfirmClick}
      >
        {guess ? "Confirmer" : "Clique sur la carte d'abord"}
      </button>
    </div>
  );
}
