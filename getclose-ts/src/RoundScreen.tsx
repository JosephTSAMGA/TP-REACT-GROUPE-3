import { useState, useEffect } from "react";
import "./RoundScreen.css";
import InteractiveMap from "./InteractiveMap";

type Coordinates = {
  lat: number;
  lng: number;
};

type RoundScreenProps = {
  imageUrl: string;
  roundNumber: number;
  totalRounds: number;
  cumulativeScore: number;
  timerSeconds?: number;
  onTimeUp?: () => void;
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
  const [timeLeft, setTimeLeft] = useState<number>(timerSeconds);

  // Nouvelle mémoire : la position choisie par le joueur sur la carte.
  // null tant qu'il n'a encore rien cliqué.
  const [guess, setGuess] = useState<Coordinates | null>(null);

  useEffect(() => {
    if (timeLeft <= 0) {
      onTimeUp();
      return;
    }
    const interval = setInterval(() => {
      setTimeLeft((prev) => prev - 1);
    }, 1000);
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
          <span className="round-timer" data-low={timeLeft <= 10}>{timeLeft}s</span>
          <span className="round-go">Go go go !</span>
        </div>
        <span className="round-cumulative">{cumulativeScore.toLocaleString("fr-FR")} pts</span>
      </header>

      <div className="round-play-area">
        <div className="round-map-space">
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