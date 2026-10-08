// =============================================================
// PARTIE 4/4 — Persistance & historique
// Fichiers de cette partie : utils/storage.ts, FinishedScreen.tsx (+.css),
// HistoryScreen.tsx (+.css).
// Rôle de ce fichier : LE point du barème "Persistance des données" —
// toutes les lectures/écritures dans le localStorage du navigateur.
// =============================================================
// Fonctions de sauvegarde/lecture dans le localStorage du navigateur.
// Contrairement à un state React classique, le localStorage n'est PAS
// effacé quand on rafraîchit la page : c'est ce qui permet de garder
// le score et l'historique des parties après un F5.

const HISTORY_KEY = "getclose_history";

// Une partie terminée, telle qu'on la stocke dans l'historique.
export type GameResult = {
  pseudo: string;
  score: number;
  playedAt: string; // date ISO, pour pouvoir l'afficher/trier plus tard
};

// Lit l'historique des parties précédentes.
// Si rien n'est stocké (première visite) ou si les données sont
// corrompues, on renvoie un tableau vide plutôt que de planter.
export function loadHistory(): GameResult[] {
  try {
    const raw = localStorage.getItem(HISTORY_KEY);
    if (!raw) return [];
    return JSON.parse(raw) as GameResult[];
  } catch {
    return [];
  }
}

// Ajoute une nouvelle partie à l'historique et sauvegarde le tout.
export function saveGameResult(pseudo: string, score: number): GameResult[] {
  const history = loadHistory();
  const updated: GameResult[] = [...history, { pseudo, score, playedAt: new Date().toISOString() }];
  localStorage.setItem(HISTORY_KEY, JSON.stringify(updated));
  return updated;
}

// Le meilleur score jamais réalisé, pratique à afficher sur l'écran de fin.
export function getBestScore(history: GameResult[]): number {
  return history.reduce((best, entry) => Math.max(best, entry.score), 0);
}
