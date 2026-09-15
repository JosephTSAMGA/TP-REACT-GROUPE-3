import "./App.css";

export default function App() {
  return (
    <main className="phase0">
      <p className="eyebrow">Phase 0 — architecture</p>
      <h1>GeoGuessr TP</h1>
      <p>
        Frontend Vite + React + TypeScript. Les écrans de jeu, la carte et l’API
        de scoring arrivent ensuite.
      </p>
      <ul>
        <li>
          Contrat API : <code>docs/api.md</code>
        </li>
        <li>
          Mocks : <code>src/shared/api/mocks</code>
        </li>
        <li>
          Backend santé : <code>http://127.0.0.1:8000/health</code>
        </li>
      </ul>
    </main>
  );
}
