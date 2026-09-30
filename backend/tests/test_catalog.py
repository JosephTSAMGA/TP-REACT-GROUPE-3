"""Lieux, catégories, et tirage de 5 lieux pour une partie."""

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.services.catalog import slugify


@pytest.fixture()
def client(tmp_path, monkeypatch):
    # Base jetable : le fichier de dev n'est pas touché par les tests.
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'test.db'}")
    with TestClient(app) as test_client:
        yield test_client


def _find(items: list[dict], key: str, value: str) -> dict:
    return next(item for item in items if item[key] == value)


def test_slugify_strips_accents() -> None:
    assert slugify("Sites naturels") == "sites-naturels"
    assert slugify("Cathédrale") == "cathedrale"


def test_seed_exposes_categories_and_locations(client: TestClient) -> None:
    response = client.get("/api/categories")
    assert response.status_code == 200
    categories = response.json()
    by_slug = {item["slug"]: item for item in categories}
    assert set(by_slug) == {"monuments", "capitales", "sites-naturels"}
    assert by_slug["monuments"]["locationCount"] == 7
    assert by_slug["capitales"]["locationCount"] == 5
    assert by_slug["sites-naturels"]["locationCount"] == 5

    locations = client.get("/api/locations")
    assert locations.status_code == 200
    assert len(locations.json()) == 17


def test_location_belongs_to_its_category(client: TestClient) -> None:
    locations = client.get("/api/locations").json()
    eiffel = next(item for item in locations if item["name"] == "Tour Eiffel")
    assert eiffel["category"]["slug"] == "monuments"
    assert eiffel["categoryId"] == eiffel["category"]["id"]

    detail = client.get(f"/api/categories/{eiffel['categoryId']}")
    assert detail.status_code == 200
    names = [item["name"] for item in detail.json()["locations"]]
    assert "Tour Eiffel" in names


def test_filter_locations_by_category(client: TestClient) -> None:
    capitales = _find(client.get("/api/categories").json(), "slug", "capitales")
    response = client.get("/api/locations", params={"categoryId": capitales["id"]})
    assert response.status_code == 200
    rows = response.json()
    assert len(rows) == capitales["locationCount"]
    assert {row["categoryId"] for row in rows} == {capitales["id"]}


def test_create_category_and_location(client: TestClient) -> None:
    created = client.post("/api/categories", json={"name": "Océans"})
    assert created.status_code == 201
    category = created.json()
    assert category["slug"] == "oceans"
    assert category["locationCount"] == 0

    location = client.post(
        "/api/locations",
        json={
            "name": "Grande barrière de corail",
            "latitude": -18.2871,
            "longitude": 147.6992,
            "imageUrl": "https://example.com/corail.jpg",
            "categoryId": category["id"],
        },
    )
    assert location.status_code == 201
    assert location.json()["category"]["slug"] == "oceans"

    detail = client.get(f"/api/categories/{category['id']}")
    names = [item["name"] for item in detail.json()["locations"]]
    assert names == ["Grande barrière de corail"]


def test_unknown_category_on_create_location(client: TestClient) -> None:
    response = client.post(
        "/api/locations",
        json={
            "name": "Nulle part",
            "latitude": 0,
            "longitude": 0,
            "imageUrl": "https://example.com/x.jpg",
            "categoryId": 9999,
        },
    )
    assert response.status_code == 404


def test_duplicate_category_name(client: TestClient) -> None:
    response = client.post("/api/categories", json={"name": "Monuments"})
    assert response.status_code == 409


def test_cannot_delete_category_that_still_has_locations(client: TestClient) -> None:
    monuments = _find(client.get("/api/categories").json(), "slug", "monuments")
    response = client.delete(f"/api/categories/{monuments['id']}")
    assert response.status_code == 409


def test_latitude_out_of_range(client: TestClient) -> None:
    category_id = client.get("/api/categories").json()[0]["id"]
    response = client.post(
        "/api/locations",
        json={
            "name": "Trop nord",
            "latitude": 120,
            "longitude": 0,
            "imageUrl": "https://example.com/x.jpg",
            "categoryId": category_id,
        },
    )
    assert response.status_code == 422


def test_move_location_to_another_category(client: TestClient) -> None:
    eiffel = _find(client.get("/api/locations").json(), "name", "Tour Eiffel")
    nature = _find(client.get("/api/categories").json(), "slug", "sites-naturels")
    response = client.put(
        f"/api/locations/{eiffel['id']}",
        json={
            "name": eiffel["name"],
            "latitude": eiffel["latitude"],
            "longitude": eiffel["longitude"],
            "imageUrl": eiffel["imageUrl"],
            "categoryId": nature["id"],
        },
    )
    assert response.status_code == 200
    assert response.json()["category"]["slug"] == "sites-naturels"


def test_random_session_picks_five_distinct_locations(client: TestClient) -> None:
    response = client.post("/api/sessions/random", json={"size": 5})
    assert response.status_code == 201
    body = response.json()
    assert body["size"] == 5
    ids = [item["id"] for item in body["locations"]]
    assert len(ids) == 5
    assert len(set(ids)) == 5

    stored = client.get(f"/api/sessions/{body['id']}")
    assert stored.status_code == 200
    assert [item["id"] for item in stored.json()["locations"]] == ids


def test_random_session_can_be_limited_to_one_category(client: TestClient) -> None:
    capitales = _find(client.get("/api/categories").json(), "slug", "capitales")
    accepted = client.post(
        "/api/sessions/random",
        json={"size": 5, "categoryId": capitales["id"]},
    )
    assert accepted.status_code == 201
    slugs = {item["category"]["slug"] for item in accepted.json()["locations"]}
    assert slugs == {"capitales"}


def test_random_session_needs_enough_locations(client: TestClient) -> None:
    created = client.post("/api/categories", json={"name": "Îles"})
    assert created.status_code == 201
    rejected = client.post(
        "/api/sessions/random",
        json={"size": 5, "categoryId": created.json()["id"]},
    )
    assert rejected.status_code == 422


def test_unknown_session(client: TestClient) -> None:
    response = client.get("/api/sessions/does-not-exist")
    assert response.status_code == 404
