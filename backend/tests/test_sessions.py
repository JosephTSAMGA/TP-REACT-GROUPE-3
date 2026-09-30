def test_create_session_requires_auth(client):
    assert client.post("/api/sessions").status_code == 401


def test_create_session_draws_rounds(client, auth_headers):
    response = client.post("/api/sessions", headers=auth_headers)
    assert response.status_code == 201
    body = response.json()
    assert body["score_total"] == 0
    assert body["finished"] is False
    assert len(body["rounds"]) == 5
    for round_ in body["rounds"]:
        assert "image_url" in round_
        assert "latitude" not in round_


def test_list_sessions_only_returns_mine(client, auth_headers):
    client.post("/api/sessions", headers=auth_headers)
    client.post("/api/sessions", headers=auth_headers)
    response = client.get("/api/sessions", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_session_score(client, auth_headers):
    created = client.post("/api/sessions", headers=auth_headers).json()
    response = client.patch(
        f"/api/sessions/{created['id']}",
        json={"score_total": 420, "finished": True},
        headers=auth_headers,
    )
    assert response.status_code == 200
    assert response.json()["score_total"] == 420
    assert response.json()["finished"] is True


def test_get_unknown_session_returns_404(client, auth_headers):
    response = client.get("/api/sessions/999999", headers=auth_headers)
    assert response.status_code == 404


def test_cannot_access_another_users_session(client, auth_headers):
    created = client.post("/api/sessions", headers=auth_headers).json()
    client.post(
        "/api/auth/register",
        json={"pseudo": "Aziz", "email": "aziz@test.com", "password": "motdepasse456"},
    )
    other_token = client.post(
        "/api/auth/login", json={"email": "aziz@test.com", "password": "motdepasse456"}
    ).json()["access_token"]
    other_headers = {"Authorization": f"Bearer {other_token}"}
    response = client.get(f"/api/sessions/{created['id']}", headers=other_headers)
    assert response.status_code == 403


def test_delete_session(client, auth_headers):
    created = client.post("/api/sessions", headers=auth_headers).json()
    response = client.delete(f"/api/sessions/{created['id']}", headers=auth_headers)
    assert response.status_code == 204
    assert client.get(f"/api/sessions/{created['id']}", headers=auth_headers).status_code == 404
