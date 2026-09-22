// =============================================================
// PARTIE 1/4 — Navigation & formulaire
// Fichiers de cette partie : App.tsx, StartScreen.tsx (+.css), NavBar.tsx (+.css).
// Rôle de ce fichier : c'est le "chef d'orchestre" de l'appli.
// Il définit les 4 pages (routes) et détient le state qui doit
// survivre quand on change de page (le pseudo du joueur, le score
// final). Il ne contient PAS la logique du jeu lui-même (ça, c'est
// dans GamePage.tsx, partie 2).
// =============================================================
import { useState } from "react";
import { Routes, Route, Navigate, useNavigate, useLocation } from "react-router-dom";
import NavBar from "./NavBar";
import StartScreen from "../features/game/StartScreen";
import GamePage from "../features/game/GamePage";
import FinishedScreen from "../features/history/FinishedScreen";
import HistoryScreen from "../features/history/HistoryScreen";
import { getBestScore, loadHistory, saveGameResult } from "../shared/storage";
import type { Round } from "../shared/types";
import "./App.css";

// Les 5 manches du jeu, avec les vraies coordonnées GPS de chaque lieu.
// C'est cette valeur "answer" qui sert de référence pour calculer la
// distance avec le point cliqué par le joueur (voir GamePage.tsx).
const mockRounds: Round[] = [
  {
    imageUrl: "https://commons.wikimedia.org/wiki/Special:FilePath/Tour%20Eiffel%20Wikimedia%20Commons%20(cropped).jpg",
    answer: { lat: 48.8584, lng: 2.2945 },
    label: "Tour Eiffel, Paris",
  },
  {
    imageUrl: "https://commons.wikimedia.org/wiki/Special:FilePath/Big%20Ben%201.jpg",
    answer: { lat: 51.5007, lng: -0.1246 },
    label: "Big Ben, Londres",
  },
  {
    imageUrl: "https://commons.wikimedia.org/wiki/Special:FilePath/The%20Colosseum.jpg",
    answer: { lat: 41.8902, lng: 12.4922 },
    label: "Colisée, Rome",
  },
  {
    imageUrl: "https://commons.wikimedia.org/wiki/Special:FilePath/Statue%20of%20Liberty.jpg",
    answer: { lat: 40.6892, lng: -74.0445 },
    label: "Statue de la Liberté, New York",
  },
  {
    imageUrl: "https://commons.wikimedia.org/wiki/Special:FilePath/SydneyOperaHouse.jpg",
    answer: { lat: -33.8568, lng: 151.2153 },
    label: "Opéra de Sydney",
  },
];

function App() {
  // Ces deux valeurs vivent dans App (au-dessus des routes) car elles
  // doivent survivre à la navigation entre "/jeu" et "/resultats".
  // React Router démonte le composant de la page précédente, mais pas
  // ses parents : le state ici n'est donc pas perdu en changeant de page.
  const [pseudo, setPseudo] = useState("");
  const [finalScore, setFinalScore] = useState<number | null>(null);

  const navigate = useNavigate();
  const location = useLocation();

  // On masque la barre de navigation pendant une manche : c'est un écran
  // immersif en plein écran qui a déjà son propre header (timer, score).
  const showNavBar = location.pathname !== "/jeu";

  const handleStart = (name: string) => {
    setPseudo(name);
    setFinalScore(null);
    navigate("/jeu");
  };

  const handleGameFinished = (score: number) => {
    // On sauvegarde la partie dans le localStorage : elle apparaîtra
    // dans l'historique et survivra à un rafraîchissement de la page.
    saveGameResult(pseudo, score);
    setFinalScore(score);
    navigate("/resultats");
  };

  return (
    <>
      {showNavBar && <NavBar />}
      {/* Table de routage : à chaque URL correspond UN composant affiché.
          C'est ce qui remplace l'ancien système "screen === 'start' ? ... : ..." */}
      <Routes>
        <Route path="/" element={<StartScreen onStart={handleStart} />} />

        {/* Accès direct à /jeu sans être passé par le formulaire : on
            renvoie vers l'accueil plutôt que de planter sur un pseudo vide. */}
        <Route
          path="/jeu"
          element={
            pseudo ? (
              <GamePage rounds={mockRounds} onFinish={handleGameFinished} />
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
                bestScore={getBestScore(loadHistory())}
                history={loadHistory()}
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
