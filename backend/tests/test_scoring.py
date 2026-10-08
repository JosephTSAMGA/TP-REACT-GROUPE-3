from app.services.scoring import distance_km, score_from_distance_km


def test_same_point_is_zero_km_and_max_score():
    assert distance_km(48.8566, 2.3522, 48.8566, 2.3522) == 0
    assert score_from_distance_km(0) == 5000


def test_farther_guess_scores_lower():
    close = score_from_distance_km(10)
    far = score_from_distance_km(2000)
    assert close > far
    assert far >= 0
