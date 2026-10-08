// =============================================================
// PARTIE 4/4 — Persistance & historique
// Fichiers de cette partie : utils/storage.ts, FinishedScreen.tsx (+.css),
// HistoryScreen.tsx (+.css).
// Rôle de ce fichier : l'écran de fin de partie, qui affiche le score
// final et le meilleur score jamais réalisé (calculé à partir de
// l'historique lu dans le localStorage par App.tsx).
// =============================================================
import "./FinishedScreen.css";
import type { GameResult } from "../../shared/storage";

type FinishedScreenProps = {
  score: number;
  bestScore: number;
  history: GameResult[];
  onReplay: () => void;
};

export default function FinishedScreen({
  score,
  bestScore,
  history,
  onReplay,
}: FinishedScreenProps) {
  const isNewBest = score > 0 && score >= bestScore;

  return (
    <div className="finished-screen">
      <div className="finished-card">
        <p className="finished-eyebrow">Partie terminée</p>
        <h1 className="finished-score">{score.toLocaleString("fr-FR")} pts</h1>

        {isNewBest ? (
          <p className="finished-best finished-best--new">Nouveau meilleur score !</p>
        ) : (
          <p className="finished-best">
            Meilleur score : {bestScore.toLocaleString("fr-FR")} pts
          </p>
        )}

        {/* Historique conservé dans le localStorage : il survit à un
            rafraîchissement de la page (contrairement à un simple state). */}
        <p className="finished-history-count">
          {history.length} partie{history.length > 1 ? "s" : ""} jouée{history.length > 1 ? "s" : ""} au total
        </p>

        <button className="finished-button" onClick={onReplay}>
          Rejouer
        </button>
      </div>
    </div>
  );
}
