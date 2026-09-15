import { useEffect, useState } from "react";
import { getRound, postGuess } from "../../shared/api";
import type { GuessResponse, RoundResponse } from "../../shared/api";
import MapPlaceholder from "./components/MapPlaceholder";
import type { LatLng } from "./components/MapPlaceholder";
import Timer from "./components/Timer";
import ScoreBoard from "./components/ScoreBoard";
import RoundResult from "./components/RoundResult";
import FinalScreen from "./components/FinalScreen";
import "./GameScreen.css";

const TOTAL_ROUNDS = 5;

// Les états possibles de l'écran. Toujours passer par l'un de ces états
// plutôt que par plusieurs booléens séparés (isLoading, isError, ...) :
// ça évite les combinaisons impossibles (ex: loading ET result en même temps).
type GameStatus =
  | "loading" // GET /round en cours
  | "playing" // manche affichée, en attente d'un clic sur la carte + Guess
  | "submitting" // POST /guess en cours
  | "result" // résultat de la manche affiché
  | "finished" // 5 manches jouées
  | "error";

export default function GameScreen() {
  const [roundIndex, setRoundIndex] = useState(0); // 0..4 -> manche 1..5
  const [status, setStatus] = useState<GameStatus>("loading");
  const [round, setRound] = useState<RoundResponse | null>(null);
  const [guess, setGuess] = useState<LatLng | null>(null);
  const [result, setResult] = useState<GuessResponse | null>(null);
  const [totalScore, setTotalScore] = useState(0);
  const [error, setError] = useState<string | null>(null);

  

 