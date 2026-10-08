import { useState } from "react";
import RoundResult from "../result/RoundResult";
import { postGuess } from "../../shared/api";
import type { Coordinates, PlayRound, RoundOutcome } from "../../shared/types";
import RoundScreen from "./RoundScreen";

type GamePageProps = {
  rounds: PlayRound[];
  onFinish: (score: number, lastGuess?: Coordinates) => void;
};

type InternalScreen = "round" | "result";

export default function GamePage({ rounds, onFinish }: GamePageProps) {
  const [roundIndex, setRoundIndex] = useState(0);
  const [score, setScore] = useState(0);
  const [screen, setScreen] = useState<InternalScreen>("round");
  const [lastOutcome, setLastOutcome] = useState<RoundOutcome | null>(null);
  const [error, setError] = useState<string | null>(null);

  const handleConfirm = async (guess: Coordinates) => {
    const round = rounds[roundIndex];
    setError(null);
    try {
      const result = await postGuess({
        round_id: round.id,
        latitude: guess.lat,
        longitude: guess.lng,
      });
      const outcome: RoundOutcome = {
        guess,
        answer: {
          imageUrl: result.actual_location.image_url,
          label: result.actual_location.name,
          answer: {
            lat: result.actual_location.latitude,
            lng: result.actual_location.longitude,
          },
        },
        distanceKm: result.distance_km,
        points: result.score,
      };
      setLastOutcome(outcome);
      setScore((prev) => prev + result.score);
      setScreen("result");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Impossible d'envoyer le guess.");
    }
  };

  const handleContinue = () => {
    const isLastRound = roundIndex + 1 >= rounds.length;
    if (isLastRound) {
      onFinish(score, lastOutcome?.guess);
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
      {error && (
        <p style={{ color: "#e2665f", textAlign: "center", margin: "0.5rem" }}>{error}</p>
      )}
      <RoundScreen
        key={roundIndex}
        imageUrl={rounds[roundIndex].image_url}
        roundNumber={roundIndex + 1}
        totalRounds={rounds.length}
        cumulativeScore={score}
        onConfirm={handleConfirm}
      />
    </div>
  );
}
