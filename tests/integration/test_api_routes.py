from src.make_a_comment.adapters.response.type import ResponseType


def test_register_user_route(api_client):

    payload = {"name": "guest",
               "email": "guest@gmail.com",
               "password": "easypass"}

    response = api_client.post("/api/v0/register_user", json=payload)

    assert response.status_code == 201

    response_json = response.get_json()

    assert response_json["name"] == payload["name"]


def test_login_route(api_client):

    payload = {"email": "guest@gmail.com",
               "password": "easypass"}

    response = api_client.post("/api/v0/login", json=payload)

    assert response.status_code == 200
    assert "access_token" in response.get_json()


def test_get_all_comments_route(api_client):

    response = api_client.get("/api/v0/get_all_comments")

    assert response.status_code == 200


def test_get_a_comment_by_uuid_route(api_client):
    payload = {"email": "guest@gmail.com",
               "password": "easypass"}

    response = api_client.post("/api/v0/login", json=payload)

    uuid = "a"*36
    response = api_client.get(f"/api/v0/get_a_comment_by_uuid/{uuid}")

    assert response.status_code == 404


def test_get_a_user_by_uuid_route(api_client):
    uuid = "a"*36
    response = api_client.get(f"/api/v0/get_a_user_by_uuid/{uuid}")

    assert response.status_code == 404


def test_logout_route(api_client):

    payload = {"email": "guest@gmail.com",
               "password": "easypass"}

    response = api_client.post("/api/v0/login", json=payload)

    assert response.status_code == 200

    response = api_client.get("/api/v0/logout")

    assert response.status_code == 200

    payload = {"text": "New Comment"}

    response = api_client.post(
        "/api/v0/make_a_comment", json=payload)  # tokenvalidation error

    assert response.status_code == 400


def test_delete_a_comment_by_uuid_route(api_client):

    payload = {"email": "guest@gmail.com",
               "password": "easypass"}

    response = api_client.post("/api/v0/login", json=payload)

    assert response.status_code == 200

    uuid = "a"*36
    response = api_client.delete(f"/api/v0/delete_a_comment_by_uuid/{uuid}")

    assert response.status_code == 404


def test_update_a_comment_route(api_client):

    payload = {"email": "guest@gmail.com",
               "password": "easypass"}

    response = api_client.post("/api/v0/login", json=payload)

    assert response.status_code == 200

    payload = {"comment_uuid": "a"*36,
               "new_text": "New text"}

    response = api_client.post("/api/v0/update_a_comment", json=payload)

    assert response.status_code == 404


def test_make_a_comment_route(api_client):

    payload = {"email": "guest@gmail.com",
               "password": "easypass"}

    response = api_client.post("/api/v0/login", json=payload)

    payload = {"text": "New Comment"}

    response = api_client.post("/api/v0/make_a_comment", json=payload)

    assert response.status_code == 201
