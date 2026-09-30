def _find(items: list[dict], key: str, value: str) -> dict:
    return next(item for item in items if item[key] == value)


def test_seed_exposes_categories_and_locations(client):
    response = client.get("/api/categories")
    assert response.status_code == 200
    by_slug = {item["slug"]: item for item in response.json()}
    assert set(by_slug) == {"monuments", "capitales", "sites-naturels"}
    locations = client.get("/api/locations")
    assert locations.status_code == 200
    assert len(locations.json()) == 17


def test_create_category_requires_auth(client):
    assert client.post("/api/categories", json={"name": "Océans"}).status_code == 401


def test_create_category_and_location(client, auth_headers):
    created = client.post("/api/categories", json={"name": "Océans"}, headers=auth_headers)
    assert created.status_code == 201
    category = created.json()
    location = client.post(
        "/api/locations",
        json={
            "name": "Grande barrière de corail",
            "latitude": -18.2871,
            "longitude": 147.6992,
            "image_url": "https://example.com/corail.jpg",
            "category_id": category["id"],
        },
        headers=auth_headers,
    )
    assert location.status_code == 201
    assert location.json()["category"]["slug"] == "oceans"


def test_unknown_category_on_create_location(client, auth_headers):
    response = client.post(
        "/api/locations",
        json={
            "name": "Nulle part",
            "latitude": 0,
            "longitude": 0,
            "image_url": "https://example.com/x.jpg",
            "category_id": 9999,
        },
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_duplicate_category_name(client, auth_headers):
    response = client.post("/api/categories", json={"name": "Monuments"}, headers=auth_headers)
    assert response.status_code == 409


def test_cannot_delete_category_that_still_has_locations(client, auth_headers):
    monuments = _find(client.get("/api/categories").json(), "slug", "monuments")
    response = client.delete(f"/api/categories/{monuments['id']}", headers=auth_headers)
    assert response.status_code == 409


def test_latitude_out_of_range(client, auth_headers):
    category_id = client.get("/api/categories").json()[0]["id"]
    response = client.post(
        "/api/locations",
        json={
            "name": "Trop nord",
            "latitude": 120,
            "longitude": 0,
            "image_url": "https://example.com/x.jpg",
            "category_id": category_id,
        },
        headers=auth_headers,
    )
    assert response.status_code == 422
