import type { GameSession } from "../types";
import type { GuessRequest, GuessResponse, TokenResponse, UserOut } from "./types";

const TOKEN_KEY = "getclose_token";

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string): void {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken(): void {
  localStorage.removeItem(TOKEN_KEY);
}

async function parseJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let detail = `${response.status} ${response.statusText}`;
    try {
      const body = await response.json();
      if (typeof body.detail === "string") detail = body.detail;
    } catch {
      /* ignore */
    }
    throw new Error(detail);
  }
  if (response.status === 204) {
    return undefined as T;
  }
  return response.json() as Promise<T>;
}

function authHeaders(): HeadersInit {
  const token = getToken();
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (token) headers.Authorization = `Bearer ${token}`;
  return headers;
}

export async function registerUser(payload: {
  pseudo: string;
  email: string;
  password: string;
}): Promise<UserOut> {
  return parseJson<UserOut>(
    await fetch("/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }),
  );
}

export async function loginUser(payload: {
  email: string;
  password: string;
}): Promise<TokenResponse> {
  const token = await parseJson<TokenResponse>(
    await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    }),
  );
  setToken(token.access_token);
  return token;
}

export async function createSession(): Promise<GameSession> {
  return parseJson<GameSession>(
    await fetch("/api/sessions", { method: "POST", headers: authHeaders() }),
  );
}

export async function listSessions(): Promise<GameSession[]> {
  return parseJson<GameSession[]>(await fetch("/api/sessions", { headers: authHeaders() }));
}

export async function finishSession(sessionId: number, scoreTotal: number): Promise<GameSession> {
  return parseJson<GameSession>(
    await fetch(`/api/sessions/${sessionId}`, {
      method: "PATCH",
      headers: authHeaders(),
      body: JSON.stringify({ finished: true, score_total: scoreTotal }),
    }),
  );
}

export async function postGuess(body: GuessRequest): Promise<GuessResponse> {
  return parseJson<GuessResponse>(
    await fetch("/api/guesses", {
      method: "POST",
      headers: authHeaders(),
      body: JSON.stringify(body),
    }),
  );
}

export async function evaluateBadges(coords?: {
  latitude: number;
  longitude: number;
}): Promise<unknown> {
  return parseJson(
    await fetch("/api/badges/evaluate", {
      method: "POST",
      headers: authHeaders(),
      body: JSON.stringify(coords ?? {}),
    }),
  );
}
