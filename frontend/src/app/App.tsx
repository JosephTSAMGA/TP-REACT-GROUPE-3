import { useState } from "react";
import StartScreen from "../features/game/components/StartScreen";
import type { GameMode } from "../features/game/components/StartScreen";
import GameScreen from "../features/game/GameScreen";

export default function App() {
  const [started, setStarted] = useState(false);

  function handleStart(mode: GameMode) {
    // Le mode est pour l'instant décoratif : l'API ne filtre pas encore par zone.
    console.log("Mode choisi :", mode);
    setStarted(true);
  }

  if (!started) {
    return <StartScreen onStart={handleStart} />;
  }

  return <GameScreen />;
}
