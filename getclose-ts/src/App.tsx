import { useState } from "react";
import StartScreen from "./StartScreen";
import RoundScreen from "./RoundScreen";

type Coordinates = { lat: number; lng: number };
type Screen = "start" | "round" | "finished";

const mockRounds = [
  { imageUrl: "https://commons.wikimedia.org/wiki/Special:FilePath/Tour%20Eiffel%20Wikimedia%20Commons%20(cropped).jpg" },
  { imageUrl: "https://commons.wikimedia.org/wiki/Special:FilePath/Big%20Ben%201.jpg" },
  { imageUrl: "https://commons.wikimedia.org/wiki/Special:FilePath/The%20Colosseum.jpg" },
  { imageUrl: "https://commons.wikimedia.org/wiki/Special:FilePath/Statue%20of%20Liberty.jpg" },
  { imageUrl: "https://commons.wikimedia.org/wiki/Special:FilePath/SydneyOperaHouse.jpg" },
];

function App() {
  const [screen, setScreen] = useState<Screen>("start");
  const [roundIndex, setRoundIndex] = useState(0);
  const [score, setScore] = useState(0);

  const handleStart = () => {
    setRoundIndex(0);
    setScore(0);
    setScreen("round");
  };

  const handleConfirm = (guess: Coordinates) => {
    console.log(`Manche ${roundIndex + 1} — guess :`, guess);
    const isLastRound = roundIndex + 1 >= mockRounds.length;
    if (isLastRound) {
      setScreen("finished");
    } else {
      setRoundIndex((prev) => prev + 1);
    }
  };

  if (screen === "start") {
    return <StartScreen onStart={handleStart} />;
  }

  if (screen === "finished") {
    return (
      <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center", background: "#0f1b2d", color: "#f2efe6" }}>
        <h1>Partie terminée ! (écran de résultat à venir)</h1>
      </div>
    );
  }

  return (
    <div style={{ minHeight: "100vh", display: "flex", flexDirection: "column", background: "#0f1b2d" }}>
      <RoundScreen
        key={roundIndex}
        imageUrl={mockRounds[roundIndex].imageUrl}
        roundNumber={roundIndex + 1}
        totalRounds={mockRounds.length}
        cumulativeScore={score}
        onConfirm={handleConfirm}
      />
    </div>
  );
}

export default App;