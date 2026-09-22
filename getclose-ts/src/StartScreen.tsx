import { useState } from "react";
import type { FormEvent } from "react";
import { PSEUDO_MAX, validatePseudo } from "./pseudo";
import Leaderboard from "./Leaderboard";
import "./StartScreen.css";

export type GameMode = "france" | "world";

type StartScreenProps = {
  onStart: (mode: GameMode, pseudo: string) => void;
};

export default function StartScreen({ onStart }: StartScreenProps) {
  const [mode, setMode] = useState<GameMode>("world");
  const [pseudo, setPseudo] = useState("");
  const [showError, setShowError] = useState(false);

  const error = validatePseudo(pseudo);

  function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (error) {
      setShowError(true);
      return;
    }
    onStart(mode, pseudo.trim());
  }

  return (
    <form className="start-screen" onSubmit={handleSubmit} noValidate>
      <p className="start-screen__eyebrow">Beta get close</p>
      <h1>Devine le lieu de la photo</h1>
      <p className="start-screen__rules">
        À chaque manche, une photo s'affiche. Clique sur la carte à l'endroit où
        tu penses qu'elle a été prise, valide ton choix, et gagne des points
        selon ta précision. 5 manches au total, additionnées en un score final.
      </p>

      {/* Choix de mode décoratif pour l'instant : GET /api/round ne prend pas
          encore de paramètre de zone. */}
      <div
        className="start-screen__mode"
        role="radiogroup"
        aria-label="Mode de jeu"
      >
        <button
          type="button"
          className={mode === "france" ? "is-selected" : ""}
          aria-pressed={mode === "france"}
          onClick={() => setMode("france")}
        >
          France
        </button>
        <button
          type="button"
          className={mode === "world" ? "is-selected" : ""}
          aria-pressed={mode === "world"}
          onClick={() => setMode("world")}
        >
          Monde
        </button>
      </div>

      <div className="start-screen__field">
        <label htmlFor="pseudo">Ton pseudo</label>
        <input
          id="pseudo"
          type="text"
          value={pseudo}
          maxLength={PSEUDO_MAX}
          placeholder="Ex : Joseph"
          autoComplete="nickname"
          aria-invalid={showError && error !== null}
          aria-describedby={showError && error ? "pseudo-error" : undefined}
          onChange={(event) => setPseudo(event.target.value)}
          onBlur={() => pseudo !== "" && setShowError(true)}
        />
        {showError && error && (
          <p id="pseudo-error" className="start-screen__error" role="alert">
            {error}
          </p>
        )}
      </div>

      <button type="submit" className="start-screen__play">
        Jouer
      </button>

      <Leaderboard />
    </form>
  );
}
