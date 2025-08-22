def test_get_posts(client):
    response = client.get("/posts")
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert all(isinstance(post, dict) for post in data)

# def test_get_post_by_id_success(client):
#     user_data = {"username": "test_user", "password": "test_password"}
#     post_data = {"title": "title", "subtitle": "subtitle", "content": "content"}
#     # Creatin a new user
#     first_response = client.post("/auth/register", json=user_data)
#     assert first_response.status_code == 201

#     # Loggin in
#     second_response = client.post("/auth/login", data=user_data)
#     data = second_response.json()
#     assert second_response.status_code == 200
    
#     token = data["access_token"]
    
#     headers = {
#         "Authorization": f"Bearer {token}",
#         "accept": "application/json"
#     }

#     # creating a new post
#     third_response = client.get("/posts/my-posts", headers=headers)
#     data = third_response.json()
#     assert third_response.status_code == 200
#     # print("RESP TEXT:", third_response.text)
#     # assert data["title"] == "title"
