export type RoundResponse = {
  id: number;
  session_id: number;
  position: number;
  image_url: string;
  guessed: boolean;
};

export type GuessRequest = {
  round_id: number;
  latitude: number;
  longitude: number;
};

export type ActualLocation = {
  id: number;
  name: string;
  latitude: number;
  longitude: number;
  image_url: string;
};

export type GuessResponse = {
  id: number;
  round_id: number;
  user_id: number;
  latitude: number;
  longitude: number;
  distance_km: number;
  score: number;
  actual_location: ActualLocation;
};

export type UserOut = {
  id: number;
  pseudo: string;
  email: string;
  created_at: string;
};

export type TokenResponse = {
  access_token: string;
  token_type: string;
  user: UserOut;
};
