def test_register_and_login(client):
    register_response = client.post(
        "/register",
        json={"username": "john", "email": "john@example.com", "password": "password123"},
    )
    assert register_response.status_code == 201
    assert register_response.json()["username"] == "john"

    login_response = client.post("/login", json={"username": "john", "password": "password123"})
    assert login_response.status_code == 200
    assert "access_token" in login_response.json()


def test_task_crud_flow_with_filter_and_pagination(client, auth_headers):
    for index in range(1, 4):
        response = client.post(
            "/tasks",
            headers=auth_headers,
            json={"title": f"Task {index}", "description": f"Description {index}"},
        )
        assert response.status_code == 201

    update_response = client.put("/tasks/1", headers=auth_headers, json={"completed": True})
    assert update_response.status_code == 200
    assert update_response.json()["completed"] is True

    list_response = client.get("/tasks?completed=true&skip=0&limit=2", headers=auth_headers)
    assert list_response.status_code == 200
    payload = list_response.json()
    assert payload["total"] == 1
    assert len(payload["items"]) == 1
    assert payload["items"][0]["completed"] is True

    delete_response = client.delete("/tasks/2", headers=auth_headers)
    assert delete_response.status_code == 204

    single_response = client.get("/tasks/2", headers=auth_headers)
    assert single_response.status_code == 404


def test_users_cannot_access_other_users_tasks(client, auth_headers):
    create_response = client.post(
        "/tasks",
        headers=auth_headers,
        json={"title": "Private Task", "description": "Visible only to owner"},
    )
    assert create_response.status_code == 201

    client.post(
        "/register",
        json={"username": "bob", "email": "bob@example.com", "password": "password123"},
    )
    bob_login = client.post("/login", json={"username": "bob", "password": "password123"})
    bob_headers = {"Authorization": f"Bearer {bob_login.json()['access_token']}"}

    response = client.get("/tasks/1", headers=bob_headers)
    assert response.status_code == 404

