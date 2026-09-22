// =============================================================
// PARTIE 4/4 — Persistance & historique
// Fichiers de cette partie : utils/storage.ts, FinishedScreen.tsx (+.css),
// HistoryScreen.tsx (+.css).
// Rôle de ce fichier : la 4ᵉ page de l'appli (/historique), qui liste
// toutes les parties précédentes. C'est la preuve la plus visuelle
// de la persistance : ferme l'onglet, rouvre-le, l'historique est
// toujours là.
// =============================================================
import { useState } from "react";
import "./HistoryScreen.css";
import { loadHistory, type GameResult } from "../../shared/storage";

// Affiche les parties précédentes, lues depuis le localStorage.
// C'est la preuve visuelle que la persistance fonctionne : les données
// sont encore là même après un rafraîchissement complet de la page.
export default function HistoryScreen() {
  // On lit le localStorage directement dans l'état initial : React Router
  // remonte ce composant à chaque fois qu'on arrive sur "/historique",
  // donc pas besoin d'un useEffect pour "resynchroniser" après coup.
  const [history] = useState<GameResult[]>(() => loadHistory());

  const sortedByDate = [...history].reverse();

  return (
    <div className="history-screen">
      <div className="history-card">
        <h1 className="history-title">Historique des parties</h1>

        {sortedByDate.length === 0 ? (
          <p className="history-empty">Aucune partie jouée pour l'instant.</p>
        ) : (
          <table className="history-table">
            <thead>
              <tr>
                <th>Joueur</th>
                <th>Score</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              {sortedByDate.map((entry, index) => (
                <tr key={index}>
                  <td>{entry.pseudo}</td>
                  <td>{entry.score.toLocaleString("fr-FR")} pts</td>
                  <td>{new Date(entry.playedAt).toLocaleString("fr-FR")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}
