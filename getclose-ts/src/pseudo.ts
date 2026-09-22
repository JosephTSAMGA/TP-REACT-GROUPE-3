export const PSEUDO_MIN = 2;
export const PSEUDO_MAX = 15;

/** Retourne un message d'erreur, ou null si le pseudo est valide. */
export function validatePseudo(value: string): string | null {
  const pseudo = value.trim();
  if (pseudo.length === 0) return "Choisis un pseudo pour jouer.";
  if (pseudo.length < PSEUDO_MIN) {
    return `Le pseudo doit faire au moins ${PSEUDO_MIN} caractères.`;
  }
  if (pseudo.length > PSEUDO_MAX) {
    return `Le pseudo ne doit pas dépasser ${PSEUDO_MAX} caractères.`;
  }
  return null;
}
