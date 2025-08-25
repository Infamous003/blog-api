def test_get_posts(client, created_post):
    response = client.get("/posts/")
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert all(isinstance(post, dict) for post in data)

def test_get_my_posts_success(client, auth_headers):
    response = client.get("/posts/my-posts", headers=auth_headers)
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert all(isinstance(post, dict) for post in data)


def test_get_post_by_id_success(client, created_post):
    id = created_post["id"]
    get_resp = client.get(f"/posts/{id}")
    data = get_resp.json()
    assert get_resp.status_code == 200
    assert data["id"] == id

def test_get_post_by_id_failure(client):
    get_resp = client.get(f"/posts/9999")
    assert get_resp.status_code == 404, "Post not found"

def test_update_post_success(client, auth_headers, created_post, updated_post):
    id = created_post["id"]
    update_resp = client.put(f"/posts/{id}", json=updated_post, headers=auth_headers)
    data = update_resp.json()
    assert update_resp.status_code == 200
    assert data["title"] == updated_post["title"]
    assert data["subtitle"] == updated_post["subtitle"]
    assert data["content"] == updated_post["content"]

def test_update_post_not_found(client, auth_headers, updated_post):
    update_resp = client.put(f"/posts/9999", json=updated_post, headers=auth_headers)
    assert update_resp.status_code == 404, "Post not found"

def test_delete_post_success(client, auth_headers, post_data, created_post):
    id = created_post["id"]
    response = client.delete(f"/posts/{id}", headers=auth_headers)
    assert response.status_code == 204

def test_delete_post_not_found(client, auth_headers):
    response = client.delete(f"/posts/9999", headers=auth_headers)
    assert response.status_code == 404

def test_get_my_posts_unauthenticated(client):
    response = client.get("/posts/my-posts")
    assert response.status_code == 401, "Not authenticated"

def test_update_post_not_unauthenticated(client, updated_post):
    update_resp = client.put(f"/posts/9999", json=updated_post)
    assert update_resp.status_code == 401, "Not authenticated"

def test_delete_post_unauthenticated(client):
    response = client.delete(f"/posts/9999")
    assert response.status_code == 401, "Not authenticated"