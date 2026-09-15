/** Types alignés sur docs/openapi.yaml. Ne pas y ajouter lat/lng dans RoundResponse. */

export type RoundResponse = {
  roundId: string;
  imageUrl: string;
  locationId: string;
};

export type GuessRequest = {
  latitude: number;
  longitude: number;
};

export type ActualLocation = {
  locationId: string;
  latitude: number;
  longitude: number;
};

export type GuessResponse = {
  distanceKm: number;
  score: number;
  actualLocation: ActualLocation;
};
