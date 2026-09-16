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

type GameStatus =
  | "loading" // Le chargement de la partie
  | "playing" // Le joueur est en train de jouer
  | "submitting" // POST /guess en cours
  | "result" // Affichage de la manche le Guess
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

  // TODO 1 — Charger une manche à chaque changement de roundIndex.
  //
  // useEffect(() => {
  //   si status === "finished", ne rien faire (return) : la partie est finie.
  //
  //   sinon :
  //     - setStatus("loading")
  //     - setGuess(null), setResult(null)  (on repart d'un état propre)
  //     - appeler getRound() (retourne une Promise<RoundResponse>)
  //     - .then((data) => { setRound(data); setStatus("playing"); })
  //     - .catch((err) => { setError(String(err)); setStatus("error"); })
  //
  // Attention : useEffect ne peut pas être `async` directement. Écris une
  // fonction async à l'intérieur et appelle-la, ou utilise .then/.catch
  // comme ci-dessus.
  //
  // }, [roundIndex]);
  //
  // Remarque : volontairement, `status` n'est PAS dans le tableau de
  // dépendances, sinon ce useEffect se relancerait aussi quand on passe en
  // "result" ou "finished".

  function handleSelectCoords(coords: LatLng) {
    // TODO 2 : n'accepter un nouveau point que si status === "playing"
    // (on ne veut pas pouvoir re-cliquer pendant "submitting" ou "result").
    // Sinon, appeler setGuess(coords).
  }

  async function handleGuess() {
    // TODO 3 :
    //   - si round est null ou guess est null : return (rien à envoyer).
    //   - setStatus("submitting")
    //   - try {
    //       const data = await postGuess(round.roundId, guess);
    //       setResult(data);
    //       setTotalScore((previous) => previous + data.score);
    //       setStatus("result");
    //     } catch (err) {
    //       setError(String(err));
    //       setStatus("playing"); // on laisse retenter le guess
    //     }
  }

  function handleNext() {
    // TODO 4 :
    //   - si roundIndex est la dernière manche (roundIndex === TOTAL_ROUNDS - 1) :
    //       setStatus("finished")
    //   - sinon :
    //       setRoundIndex((previous) => previous + 1)
    //       (le useEffect du TODO 1 se charge de recharger une manche tout
    //       seul, puisque roundIndex change)
  }

  function handleRestart() {
    // TODO 5 : remettre la partie à zéro :
    //   - setTotalScore(0)
    //   - setRoundIndex(0)
    //   - setStatus("loading")
    // Piège : si roundIndex était déjà à 0 (ex. la partie n'a fait qu'une
    // manche avant de planter), le useEffect du TODO 1 ne se redéclenche
    // PAS automatiquement puisque la valeur ne change pas. Il faut donc
    // aussi relancer le chargement explicitement ici (dupliquer l'appel à
    // getRound, ou restructurer le useEffect pour qu'il dépende aussi d'un
    // compteur de "tentative" que tu incrémentes à chaque restart).
  }

  if (status === "error") {
    return <p role="alert">Une erreur est survenue : {error}</p>;
  }

  if (status === "finished") {
    return (
      <FinalScreen
        totalScore={totalScore}
        totalRounds={TOTAL_ROUNDS}
        onRestart={handleRestart}
      />
    );
  }

  if (status === "loading" || !round) {
    return <p>Chargement de la manche…</p>;
  }

  return (
    <div className="game-screen">
      <ScoreBoard
        roundNumber={roundIndex + 1}
        totalRounds={TOTAL_ROUNDS}
        totalScore={totalScore}
      />

      <Timer roundKey={round.roundId} running={status === "playing"} />

      {/* TODO 6 : afficher la photo de la manche :
          <img className="game-screen__photo" src={round.imageUrl} alt="Lieu à deviner" /> */}

      <MapPlaceholder
        guess={guess}
        actualLocation={result ? result.actualLocation : null}
        onSelect={handleSelectCoords}
        disabled={status !== "playing"}
      />

      {/* TODO 7 :
          - si status === "result" ET result n'est pas null :
              afficher <RoundResult
                result={result}
                isLastRound={roundIndex === TOTAL_ROUNDS - 1}
                onNext={handleNext}
              />
          - sinon :
              afficher un <button type="button" onClick={handleGuess}
                disabled={!guess || status !== "playing"}>Guess</button> */}
    </div>
  );
}
