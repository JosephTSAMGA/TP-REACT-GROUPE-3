export type Coordinates = {
  lat: number;
  lng: number;
};

export type PlayRound = {
  id: number;
  session_id: number;
  position: number;
  image_url: string;
  guessed: boolean;
};

export type GameSession = {
  id: number;
  user_id: number;
  score_total: number;
  finished: boolean;
  started_at: string;
  finished_at: string | null;
  rounds: PlayRound[];
};

export type AuthUser = {
  id: number;
  pseudo: string;
  email: string;
};

export type RoundOutcome = {
  guess: Coordinates;
  answer: {
    imageUrl: string;
    label: string;
    answer: Coordinates;
  };
  distanceKm: number;
  points: number;
};
