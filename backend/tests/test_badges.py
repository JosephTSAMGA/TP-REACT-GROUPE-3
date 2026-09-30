# =============================================================
# Tests de /badges — catalogue public, déblocage, idempotence, et
# intégration Nominatim (mockée : on ne fait pas de vrai appel réseau).
# =============================================================
from unittest.mock import patch

import pytest

from app.database import SessionLocal
from app.seed_badges import seed_badges_if_empty


@pytest.fixture(autouse=True)
def seed_catalog(reset_database):
    """`reset_database` (conftest.py) vide les tables avant chaque test,
    y compris le catalogue de badges rempli au démarrage de l'appli.
    On le re-remplit ici pour que chaque test parte d'un catalogue non
    vide, comme en conditions réelles."""
    db = SessionLocal()
    try:
        seed_badges_if_empty(db)
    finally:
        db.close()


@pytest.fixture()
def auth_headers(client):
    client.post(
        "/auth/register",
        json={
            "pseudo": "Zouzou",
            "email": "zouzou@test.com",
            "password": "motdepasse123",
        },
    )
    response = client.post(
        "/auth/login", json={"email": "zouzou@test.com", "password": "motdepasse123"}
    )
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_catalog_is_public(client):
    response = client.get("/badges")
    assert response.status_code == 200
    codes = {badge["code"] for badge in response.json()}
    assert "premiere_partie" in codes


def test_my_badges_requires_auth(client):
    response = client.get("/badges/me")
    assert response.status_code == 401


def test_no_badge_before_playing(client, auth_headers):
    response = client.get("/badges/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_first_game_unlocks_badge(client, auth_headers):
    created = client.post("/sessions", headers=auth_headers).json()
    client.patch(
        f"/sessions/{created['id']}",
        json={"finished": True, "score_total": 1000},
        headers=auth_headers,
    )

    response = client.post("/badges/evaluate", json={}, headers=auth_headers)
    assert response.status_code == 200
    codes = {entry["badge"]["code"] for entry in response.json()}
    assert codes == {"premiere_partie"}


def test_evaluate_is_idempotent(client, auth_headers):
    created = client.post("/sessions", headers=auth_headers).json()
    client.patch(
        f"/sessions/{created['id']}",
        json={"finished": True, "score_total": 1000},
        headers=auth_headers,
    )

    client.post("/badges/evaluate", json={}, headers=auth_headers)
    second = client.post("/badges/evaluate", json={}, headers=auth_headers)

    # Rien de nouveau à débloquer la deuxième fois.
    assert second.json() == []
    my_badges = client.get("/badges/me", headers=auth_headers).json()
    assert len(my_badges) == 1


def test_high_score_unlocks_elite_badge(client, auth_headers):
    created = client.post("/sessions", headers=auth_headers).json()
    client.patch(
        f"/sessions/{created['id']}",
        json={"finished": True, "score_total": 21000},
        headers=auth_headers,
    )

    response = client.post("/badges/evaluate", json={}, headers=auth_headers)
    codes = {entry["badge"]["code"] for entry in response.json()}
    assert "voyageur_elite" in codes


@patch("app.services.badges.reverse_geocode", return_value="Paris, France")
def test_explorer_badge_uses_geocoding(mock_geocode, client, auth_headers):
    response = client.post(
        "/badges/evaluate",
        json={"latitude": 48.8566, "longitude": 2.3522},
        headers=auth_headers,
    )
    assert response.status_code == 200
    body = response.json()
    assert body[0]["badge"]["code"] == "explorateur_international"
    assert body[0]["unlocked_place"] == "Paris, France"
    mock_geocode.assert_called_once_with(48.8566, 2.3522)


@patch("app.services.badges.reverse_geocode", side_effect=ValueError("pas d'adresse"))
def test_explorer_badge_skipped_if_geocoding_fails(mock_geocode, client, auth_headers):
    response = client.post(
        "/badges/evaluate",
        json={"latitude": 0.0, "longitude": 0.0},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json() == []
