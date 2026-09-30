import { useState } from "react";
import { Routes, Route, Navigate, useNavigate, useLocation } from "react-router-dom";
import NavBar from "./NavBar";
import StartScreen, { type StartPayload } from "../features/game/StartScreen";
import GamePage from "../features/game/GamePage";
import FinishedScreen from "../features/history/FinishedScreen";
import HistoryScreen from "../features/history/HistoryScreen";
import {
  createSession,
  evaluateBadges,
  finishSession,
  loginUser,
  registerUser,
} from "../shared/api";
import { getBestScore, saveGameResult, type GameResult } from "../shared/storage";
import type { Coordinates, GameSession } from "../shared/types";
import "./App.css";

function App() {
  const [pseudo, setPseudo] = useState("");
  const [finalScore, setFinalScore] = useState<number | null>(null);
  const [history, setHistory] = useState<GameResult[]>([]);
  const [session, setSession] = useState<GameSession | null>(null);

  const navigate = useNavigate();
  const location = useLocation();
  const showNavBar = location.pathname !== "/jeu";

  const handleStart = async (payload: StartPayload) => {
    if (payload.mode === "register") {
      await registerUser({
        pseudo: payload.pseudo,
        email: payload.email,
        password: payload.password,
      });
    }
    const token = await loginUser({ email: payload.email, password: payload.password });
    const game = await createSession();
    setPseudo(token.user.pseudo);
    setSession(game);
    setFinalScore(null);
    navigate("/jeu");
  };

  const handleGameFinished = async (score: number, lastGuess?: Coordinates) => {
    if (session) {
      await finishSession(session.id, score);
      await evaluateBadges(
        lastGuess ? { latitude: lastGuess.lat, longitude: lastGuess.lng } : undefined,
      );
    }
    const updated = saveGameResult(pseudo, score);
    setHistory(updated);
    setFinalScore(score);
    navigate("/resultats");
  };

  return (
    <>
      {showNavBar && <NavBar />}
      <Routes>
        <Route path="/" element={<StartScreen onStart={handleStart} />} />
        <Route
          path="/jeu"
          element={
            session ? (
              <GamePage rounds={session.rounds} onFinish={handleGameFinished} />
            ) : (
              <Navigate to="/" replace />
            )
          }
        />
        <Route
          path="/resultats"
          element={
            finalScore !== null ? (
              <FinishedScreen
                score={finalScore}
                bestScore={getBestScore(history)}
                history={history}
                onReplay={() => navigate("/")}
              />
            ) : (
              <Navigate to="/" replace />
            )
          }
        />
        <Route path="/historique" element={<HistoryScreen />} />
      </Routes>
    </>
  );
}

export default App;
