import { useState } from "react";
import "./StartScreen.css";

export type GameMode = "france" | "world";

type StartScreenProps = {
  onStart: (mode: GameMode) => void;
};

export default function StartScreen({ onStart }: StartScreenProps) {
  const [mode, setMode] = useState<GameMode>("world");

  return (
    <div className="start-screen">
      <p className="start-screen__eyebrow">GeoGuessr TP</p>
      <h1>Devine le lieu de la photo</h1>
      <p className="start-screen__rules">
        À chaque manche, une photo s'affiche. Clique sur la carte à
        l'endroit où tu penses qu'elle a été prise, valide ton choix, et
        gagne des points selon ta précision. 5 manches au total, additionnées
        en un score final.
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

      <button
        type="button"
        className="start-screen__play"
        onClick={() => onStart(mode)}
      >
        Jouer
      </button>
    </div>
  );
}
