"""Distance (Haversine) et score. Implémentation : P2. Tests : P5.

score = max(0, round(5000 * exp(-distance_km / 2000)))
distance_km arrondie à 1 décimale.
"""


def distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    raise NotImplementedError


def score_from_distance_km(distance: float) -> int:
    raise NotImplementedError
