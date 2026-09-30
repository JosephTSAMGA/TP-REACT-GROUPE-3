// Client des ressources Category et Location, et du tirage d'une partie.
// Le score reste calculé dans le navigateur : une session renvoie donc
// les coordonnées, contrairement à GET /api/round qui les cache.
import type { Round } from "../types";

export type CategoryBrief = {
  id: number;
  name: string;
  slug: string;
};

export type Category = CategoryBrief & {
  locationCount: number;
};

export type SessionLocation = {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  imageUrl: string;
  categoryId: number;
  category: CategoryBrief;
};

export type GameSession = {
  id: string;
  createdAt: string;
  size: number;
  categoryId: number | null;
  locations: SessionLocation[];
};

export class ApiError extends Error {
  status: number;

  constructor(status: number, message: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

async function readError(response: Response): Promise<ApiError> {
  let detail = response.statusText;
  try {
    const payload = (await response.json()) as { detail?: unknown };
    if (typeof payload.detail === "string") {
      detail = payload.detail;
    }
  } catch {
    // Le corps n'est pas du JSON : on garde le statut HTTP.
  }
  return new ApiError(response.status, detail);
}

export async function listCategories(): Promise<Category[]> {
  const response = await fetch("/api/categories");
  if (!response.ok) {
    throw await readError(response);
  }
  return response.json() as Promise<Category[]>;
}

// Ouvre une partie. Sans categoryId, le tirage mélange tous les thèmes.
export async function createRandomSession(options: {
  size?: number;
  categoryId?: number | null;
}): Promise<GameSession> {
  const body: { size: number; categoryId?: number } = {
    size: options.size ?? 5,
  };
  if (options.categoryId != null) {
    body.categoryId = options.categoryId;
  }

  const response = await fetch("/api/sessions/random", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(body),
  });
  if (!response.ok) {
    throw await readError(response);
  }
  return response.json() as Promise<GameSession>;
}

// Forme attendue par GamePage : photo, vraie position, libellé affiché
// après la manche. Le thème est dans le libellé pour garder la relation visible.
export function sessionToRounds(session: GameSession): Round[] {
  return session.locations.map((location) => ({
    imageUrl: location.imageUrl,
    answer: { lat: location.latitude, lng: location.longitude },
    label: `${location.name} · ${location.category.name}`,
  }));
}
