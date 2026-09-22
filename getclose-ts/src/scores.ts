const STORAGE_KEY = "beta-get-close:scores";
const MAX_SCORES = 5;

export type ScoreEntry = {
  pseudo: string;
  score: number;
  date: string; // ISO
};

function isScoreEntry(value: unknown): value is ScoreEntry {
  if (typeof value !== "object" || value === null) return false;
  const entry = value as Record<string, unknown>;
  return (
    typeof entry.pseudo === "string" &&
    typeof entry.score === "number" &&
    typeof entry.date === "string"
  );
}

/** Lit les meilleurs scores. Retourne [] si le storage est absent ou corrompu. */
export function loadScores(): ScoreEntry[] {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return [];
    const parsed: unknown = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed.filter(isScoreEntry) : [];
  } catch {
    return [];
  }
}

/** Ajoute un score, garde les MAX_SCORES meilleurs et retourne la liste. */
export function saveScore(pseudo: string, score: number): ScoreEntry[] {
  const scores = [
    ...loadScores(),
    { pseudo, score, date: new Date().toISOString() },
  ]
    .sort((a, b) => b.score - a.score)
    .slice(0, MAX_SCORES);

  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(scores));
  } catch {
    // Storage plein ou bloqué : le jeu continue, le score n'est juste pas gardé.
  }
  return scores;
}
