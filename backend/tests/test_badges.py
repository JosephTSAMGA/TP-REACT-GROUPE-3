from unittest.mock import patch

import pytest

from app.database import SessionLocal
from app.seed_badges import seed_badges_if_empty


@pytest.fixture(autouse=True)
def seed_catalog(reset_database):
    db = SessionLocal()
    try:
        seed_badges_if_empty(db)
    finally:
        db.close()


def test_catalog_is_public(client):
    response = client.get("/api/badges")
    assert response.status_code == 200
    codes = {badge["code"] for badge in response.json()}
    assert "premiere_partie" in codes


def test_my_badges_requires_auth(client):
    assert client.get("/api/badges/me").status_code == 401


def test_no_badge_before_playing(client, auth_headers):
    response = client.get("/api/badges/me", headers=auth_headers)
    assert response.status_code == 200
    assert response.json() == []


def test_first_game_unlocks_badge(client, auth_headers):
    created = client.post("/api/sessions", headers=auth_headers).json()
    client.patch(
        f"/api/sessions/{created['id']}",
        json={"finished": True, "score_total": 1000},
        headers=auth_headers,
    )
    response = client.post("/api/badges/evaluate", json={}, headers=auth_headers)
    assert response.status_code == 200
    codes = {entry["badge"]["code"] for entry in response.json()}
    assert codes == {"premiere_partie"}


def test_evaluate_is_idempotent(client, auth_headers):
    created = client.post("/api/sessions", headers=auth_headers).json()
    client.patch(
        f"/api/sessions/{created['id']}",
        json={"finished": True, "score_total": 1000},
        headers=auth_headers,
    )
    client.post("/api/badges/evaluate", json={}, headers=auth_headers)
    second = client.post("/api/badges/evaluate", json={}, headers=auth_headers)
    assert second.json() == []
    my_badges = client.get("/api/badges/me", headers=auth_headers).json()
    assert len(my_badges) == 1


def test_high_score_unlocks_elite_badge(client, auth_headers):
    created = client.post("/api/sessions", headers=auth_headers).json()
    client.patch(
        f"/api/sessions/{created['id']}",
        json={"finished": True, "score_total": 21000},
        headers=auth_headers,
    )
    response = client.post("/api/badges/evaluate", json={}, headers=auth_headers)
    codes = {entry["badge"]["code"] for entry in response.json()}
    assert "voyageur_elite" in codes


@patch("app.services.badges.reverse_geocode", return_value="Paris, France")
def test_explorer_badge_uses_geocoding(mock_geocode, client, auth_headers):
    response = client.post(
        "/api/badges/evaluate",
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
        "/api/badges/evaluate",
        json={"latitude": 0.0, "longitude": 0.0},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json() == []


def test_badge_crud(client, auth_headers):
    created = client.post(
        "/api/badges",
        json={"code": "test_badge", "name": "Test", "description": "Un badge de test."},
        headers=auth_headers,
    )
    assert created.status_code == 201
    badge_id = created.json()["id"]
    assert client.get(f"/api/badges/{badge_id}").status_code == 200
    updated = client.put(
        f"/api/badges/{badge_id}",
        json={"code": "test_badge", "name": "Test 2", "description": "Modifié."},
        headers=auth_headers,
    )
    assert updated.json()["name"] == "Test 2"
    assert client.delete(f"/api/badges/{badge_id}", headers=auth_headers).status_code == 204
