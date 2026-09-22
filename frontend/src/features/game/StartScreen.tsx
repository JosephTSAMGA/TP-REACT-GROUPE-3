// =============================================================
// PARTIE 1/4 — Navigation & formulaire
// Fichiers de cette partie : App.tsx, StartScreen.tsx (+.css), NavBar.tsx (+.css).
// Rôle de ce fichier : la page d'accueil, avec le SEUL formulaire de
// l'application (le barème demande un formulaire avec input contrôlé,
// validation et messages d'erreur — tout est ici).
// =============================================================
import { useState, type FormEvent } from "react";
import "./StartScreen.css";

type StartScreenProps = {
  onStart: (pseudo: string) => void;
};

const MIN_LENGTH = 2;
const MAX_LENGTH = 20;

// Vérifie le pseudo et renvoie un message d'erreur, ou null si tout va bien.
// On centralise la règle ici pour ne pas la dupliquer entre l'affichage
// en direct (pendant la frappe) et la validation à la soumission.
function validatePseudo(pseudo: string): string | null {
  const trimmed = pseudo.trim();
  if (trimmed.length === 0) return "Le pseudo est obligatoire.";
  if (trimmed.length < MIN_LENGTH) return `Le pseudo doit faire au moins ${MIN_LENGTH} caractères.`;
  if (trimmed.length > MAX_LENGTH) return `Le pseudo doit faire au plus ${MAX_LENGTH} caractères.`;
  return null;
}

export default function StartScreen({ onStart }: StartScreenProps) {
  // Champ contrôlé : la valeur de l'input vit dans le state React,
  // pas dans le DOM (c'est ce qui définit un "input contrôlé").
  const [pseudo, setPseudo] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    // Empêche le comportement par défaut du navigateur (rechargement
    // de la page à la soumission d'un <form>).
    event.preventDefault();

    const validationError = validatePseudo(pseudo);
    if (validationError) {
      setError(validationError);
      return;
    }

    setError(null);
    onStart(pseudo.trim());
  };

  return (
    <div className="start-screen">
      <div className="start-content">
        <p className="start-eyebrow">Jeu de géographie</p>
        <h1 className="start-title">GetClose</h1>
        <p className="start-tagline">
          Une photo, une carte, cinq manches. Devine où tu es, le plus près possible.
        </p>

        <form className="start-form" onSubmit={handleSubmit} noValidate>
          <label className="start-label" htmlFor="pseudo">
            Ton pseudo
          </label>
          <input
            id="pseudo"
            className="start-input"
            type="text"
            value={pseudo}
            onChange={(event) => setPseudo(event.target.value)}
            placeholder="ex : Zouzou"
            aria-invalid={error !== null}
            aria-describedby={error ? "pseudo-error" : undefined}
          />
          {error && (
            <p id="pseudo-error" className="start-error">
              {error}
            </p>
          )}

          <button className="start-button" type="submit">
            Jouer
          </button>
        </form>
      </div>
    </div>
  );
}
