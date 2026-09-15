import guessMock from "./mocks/guess.json";
import roundMock from "./mocks/round.json";
import type { GuessRequest, GuessResponse, RoundResponse } from "./types";

const useMocks = import.meta.env.VITE_USE_MOCKS !== "false";

async function parseJson<T>(response: Response): Promise<T> {
  if (!response.ok) {
    throw new Error(`${response.status} ${response.statusText}`);
  }
  return response.json() as Promise<T>;
}

export async function getRound(): Promise<RoundResponse> {
  if (useMocks) {
    return roundMock;
  }
  return parseJson<RoundResponse>(await fetch("/api/round"));
}

export async function postGuess(
  roundId: string,
  body: GuessRequest,
): Promise<GuessResponse> {
  if (useMocks) {
    return guessMock;
  }
  return parseJson<GuessResponse>(
    await fetch(`/api/round/${roundId}/guess`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    }),
  );
}
