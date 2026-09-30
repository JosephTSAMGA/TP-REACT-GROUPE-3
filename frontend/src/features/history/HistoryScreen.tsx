import { useEffect, useState } from "react";
import "./HistoryScreen.css";
import { listSessions } from "../../shared/api";
import { loadHistory, type GameResult } from "../../shared/storage";

export default function HistoryScreen() {
  const [history, setHistory] = useState<GameResult[]>(() => loadHistory());
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    listSessions()
      .then((sessions) => {
        setHistory(
          sessions.map((session) => ({
            pseudo: "Toi",
            score: session.score_total,
            playedAt: session.started_at,
          })),
        );
      })
      .catch(() => {
        setError("Historique serveur indisponible, affichage local.");
      });
  }, []);

  const sortedByDate = [...history].reverse();

  return (
    <div className="history-screen">
      <div className="history-card">
        <h1 className="history-title">Historique des parties</h1>
        {error && <p className="history-empty">{error}</p>}

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
                <tr key={`${entry.playedAt}-${index}`}>
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
