def test_api(api_client):

    payload = {"name": "new guest",
               "email": "new_guest@gmail.com",
               "password": "easypass"}

    response = api_client.post("/api/v0/register_user", json=payload)

    assert response.status_code == 201

    payload = {"email": "new_guest@gmail.com",
               "password": "easypass"}

    response = api_client.post("/api/v0/login", json=payload)

    assert response.status_code == 200

    response = api_client.get("/api/v0/view_all_comments")

    assert response.status_code == 200

    payload = {"text": "New Comment"}

    response = api_client.post("/api/v0/make_a_comment", json=payload)

    comment_uuid = response.json["uuid"]

    assert response.status_code == 201

    response = api_client.get(f"/api/v0/get_a_comment_by_uuid/{comment_uuid}")

    comment = response.json

    assert comment["uuid"] == comment_uuid
    assert comment["text"] == payload["text"]
