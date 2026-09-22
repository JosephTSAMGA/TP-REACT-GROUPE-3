// =============================================================
// PARTIE 2/4 — Le cœur du jeu (carte & manches)
// Fichiers de cette partie : GamePage.tsx, RoundScreen.tsx (+.css),
// InteractiveMap.tsx.
// Rôle de ce fichier : c'est le "cerveau" d'une partie. Il connaît
// les 5 manches et LA bonne réponse de chacune (contrairement à
// RoundScreen qui ne voit que la question). C'est ici qu'on appelle
// les fonctions de la partie 3 (scoring.ts) pour transformer un clic
// sur la carte en points.
// =============================================================
import { useState } from "react";
import RoundResult from "../result/RoundResult";
import { computeScore, haversineDistanceKm } from "../../shared/scoring";
import type { Coordinates, Round, RoundOutcome } from "../../shared/types";
import RoundScreen from "./RoundScreen";

type GamePageProps = {
  rounds: Round[];
  // Appelé une fois la dernière manche terminée, avec le score final.
  onFinish: (score: number) => void;
};

// À l'intérieur d'une partie, on alterne juste entre "round" (le joueur
// joue la manche) et "result" (on lui montre ce qu'il a gagné). Ces deux
// écrans ne méritent pas leur propre URL : ils font partie de la même
// session de jeu continue.
type InternalScreen = "round" | "result";

export default function GamePage({ rounds, onFinish }: GamePageProps) {
  const [roundIndex, setRoundIndex] = useState(0);
  const [score, setScore] = useState(0);
  const [screen, setScreen] = useState<InternalScreen>("round");
  const [lastOutcome, setLastOutcome] = useState<RoundOutcome | null>(null);

  // Appelé quand le joueur confirme sa position sur la carte : on compare
  // son point (guess) au vrai lieu pour calculer une distance, puis un score.
  const handleConfirm = (guess: Coordinates) => {
    const round = rounds[roundIndex];
    const distanceKm = haversineDistanceKm(guess, round.answer);
    const points = computeScore(distanceKm);

    setLastOutcome({ guess, answer: round, distanceKm, points });
    setScore((prev) => prev + points);
    setScreen("result");
  };

  // Depuis l'écran de résultat : manche suivante, ou fin de partie.
  const handleContinue = () => {
    const isLastRound = roundIndex + 1 >= rounds.length;
    if (isLastRound) {
      onFinish(score);
    } else {
      setRoundIndex((prev) => prev + 1);
      setScreen("round");
    }
  };

  if (screen === "result" && lastOutcome) {
    return (
      <RoundResult
        outcome={lastOutcome}
        cumulativeScore={score}
        isLastRound={roundIndex + 1 >= rounds.length}
        onContinue={handleContinue}
      />
    );
  }

  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column", background: "#0f1b2d" }}>
      <RoundScreen
        key={roundIndex}
        imageUrl={rounds[roundIndex].imageUrl}
        roundNumber={roundIndex + 1}
        totalRounds={rounds.length}
        cumulativeScore={score}
        onConfirm={handleConfirm}
      />
    </div>
  );
}
