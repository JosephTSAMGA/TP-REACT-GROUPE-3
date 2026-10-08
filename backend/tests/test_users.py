def test_users_require_auth(client):
    assert client.get("/api/users").status_code == 401


def test_me_and_list(client, auth_headers):
    me = client.get("/api/users/me", headers=auth_headers)
    assert me.status_code == 200
    assert me.json()["pseudo"] == "Zouzou"

    listing = client.get("/api/users", headers=auth_headers)
    assert listing.status_code == 200
    assert any(user["email"] == "zouzou@test.com" for user in listing.json())


def test_get_unknown_user(client, auth_headers):
    response = client.get("/api/users/999999", headers=auth_headers)
    assert response.status_code == 404


def test_update_and_delete_me(client, auth_headers):
    updated = client.patch(
        "/api/users/me", json={"pseudo": "Zouzou2"}, headers=auth_headers
    )
    assert updated.status_code == 200
    assert updated.json()["pseudo"] == "Zouzou2"

    deleted = client.delete("/api/users/me", headers=auth_headers)
    assert deleted.status_code == 204
    assert client.get("/api/users/me", headers=auth_headers).status_code == 401
