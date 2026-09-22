import { useState } from "react";
import { loadScores } from "./scores";
import "./Leaderboard.css";

export default function Leaderboard() {
  // Lecture au montage : l'écran final se monte après la sauvegarde du score.
  const [scores] = useState(loadScores);

  return (
    <section className="leaderboard">
      <h2>Meilleurs scores</h2>
      {scores.length === 0 ? (
        <p className="leaderboard__empty">- - -</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th scope="col">#</th>
              <th scope="col">Joueur</th>
              <th scope="col">Score</th>
              <th scope="col">Date</th>
            </tr>
          </thead>
          <tbody>
            {scores.map((entry, index) => (
              <tr key={entry.date}>
                <td>{index + 1}</td>
                <td>{entry.pseudo}</td>
                <td>{entry.score}</td>
                <td>{new Date(entry.date).toLocaleDateString("fr-FR")}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </section>
  );
}
