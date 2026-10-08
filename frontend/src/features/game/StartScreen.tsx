import { useState, type FormEvent } from "react";
import "./StartScreen.css";

export type StartPayload = {
  mode: "register" | "login";
  pseudo: string;
  email: string;
  password: string;
};

type StartScreenProps = {
  onStart: (payload: StartPayload) => Promise<void> | void;
};

const MIN_LENGTH = 2;
const MAX_LENGTH = 20;

function validatePseudo(pseudo: string): string | null {
  const trimmed = pseudo.trim();
  if (trimmed.length === 0) return "Le pseudo est obligatoire.";
  if (trimmed.length < MIN_LENGTH) return `Le pseudo doit faire au moins ${MIN_LENGTH} caractères.`;
  if (trimmed.length > MAX_LENGTH) return `Le pseudo doit faire au plus ${MAX_LENGTH} caractères.`;
  return null;
}

export default function StartScreen({ onStart }: StartScreenProps) {
  const [mode, setMode] = useState<"register" | "login">("register");
  const [pseudo, setPseudo] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState(false);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (mode === "register") {
      const validationError = validatePseudo(pseudo);
      if (validationError) {
        setError(validationError);
        return;
      }
    }
    if (!email.trim() || !password) {
      setError("Email et mot de passe sont obligatoires.");
      return;
    }
    if (password.length < 8) {
      setError("Le mot de passe doit faire au moins 8 caractères.");
      return;
    }

    setError(null);
    setPending(true);
    try {
      await onStart({
        mode,
        pseudo: pseudo.trim(),
        email: email.trim(),
        password,
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Connexion impossible.");
    } finally {
      setPending(false);
    }
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
          {mode === "register" && (
            <>
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
              />
            </>
          )}

          <label className="start-label" htmlFor="email">
            Email
          </label>
          <input
            id="email"
            className="start-input"
            type="email"
            value={email}
            onChange={(event) => setEmail(event.target.value)}
            placeholder="ex : zouzou@test.com"
          />

          <label className="start-label" htmlFor="password">
            Mot de passe
          </label>
          <input
            id="password"
            className="start-input"
            type="password"
            value={password}
            onChange={(event) => setPassword(event.target.value)}
            placeholder="8 caractères minimum"
          />

          {error && (
            <p id="pseudo-error" className="start-error">
              {error}
            </p>
          )}

          <button className="start-button" type="submit" disabled={pending}>
            {pending ? "Chargement…" : mode === "register" ? "Créer un compte et jouer" : "Connexion et jouer"}
          </button>
        </form>

        <button
          type="button"
          className="start-switch"
          onClick={() => {
            setMode((current) => (current === "register" ? "login" : "register"));
            setError(null);
          }}
        >
          {mode === "register" ? "J'ai déjà un compte" : "Créer un compte"}
        </button>
      </div>
    </div>
  );
}
