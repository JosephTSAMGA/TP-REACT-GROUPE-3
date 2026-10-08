def test_guess_round_trip(client, auth_headers):
    session = client.post("/api/sessions", headers=auth_headers).json()
    round_ = session["rounds"][0]
    assert "latitude" not in round_

    guess = client.post(
        "/api/guesses",
        json={"round_id": round_["id"], "latitude": 48.8584, "longitude": 2.2945},
        headers=auth_headers,
    )
    assert guess.status_code == 201
    body = guess.json()
    assert "actual_location" in body
    assert "latitude" in body["actual_location"]
    assert body["score"] >= 0

    duplicate = client.post(
        "/api/guesses",
        json={"round_id": round_["id"], "latitude": 0, "longitude": 0},
        headers=auth_headers,
    )
    assert duplicate.status_code == 409


def test_guess_unknown_round(client, auth_headers):
    response = client.post(
        "/api/guesses",
        json={"round_id": 999999, "latitude": 0, "longitude": 0},
        headers=auth_headers,
    )
    assert response.status_code == 404


def test_guess_rejects_invalid_lat(client, auth_headers):
    session = client.post("/api/sessions", headers=auth_headers).json()
    response = client.post(
        "/api/guesses",
        json={"round_id": session["rounds"][0]["id"], "latitude": 200, "longitude": 0},
        headers=auth_headers,
    )
    assert response.status_code == 422


def test_list_and_delete_guess(client, auth_headers):
    session = client.post("/api/sessions", headers=auth_headers).json()
    created = client.post(
        "/api/guesses",
        json={"round_id": session["rounds"][0]["id"], "latitude": 10, "longitude": 10},
        headers=auth_headers,
    ).json()
    listing = client.get("/api/guesses", headers=auth_headers)
    assert listing.status_code == 200
    assert len(listing.json()) == 1
    assert client.delete(f"/api/guesses/{created['id']}", headers=auth_headers).status_code == 204


def test_round_get_one(client, auth_headers):
    session = client.post("/api/sessions", headers=auth_headers).json()
    round_id = session["rounds"][0]["id"]
    response = client.get(f"/api/rounds/{round_id}", headers=auth_headers)
    assert response.status_code == 200
    assert "latitude" not in response.json()
    assert client.get("/api/rounds/999999", headers=auth_headers).status_code == 404
