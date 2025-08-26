def test_like_post_success(client, created_post, auth_headers):
    id = created_post["id"]
    response = client.post(f"/posts/{id}/like", headers=auth_headers)

    assert response.status_code == 201

def test_like_post_conflict(client, created_post, auth_headers):
    id = created_post["id"]
    response = client.post(f"/posts/{id}/like", headers=auth_headers)
    assert response.status_code == 201

    response = client.post(f"/posts/{id}/like", headers=auth_headers)
    assert response.status_code == 409, "You have already liked this post"

def test_like_post_not_found(client, auth_headers):
    response = client.post(f"/posts/9999/like", headers=auth_headers)
    assert response.status_code == 404, "Post not found"

def test_like_post_unauthenticated(client, created_post):
    id = created_post["id"]
    response = client.post(f"/posts/{id}/like")
    assert response.status_code == 401, "Not authenticated"



def test_unlike_post_success(client, created_post, auth_headers):
    id = created_post["id"]
    response = client.post(f"/posts/{id}/like", headers=auth_headers)
    assert response.status_code == 201

    response = client.delete(f"/posts/{id}/like", headers=auth_headers)
    assert response.status_code == 204

def test_unlike_post_conflict(client, created_post, auth_headers):
    id = created_post["id"]
    response = client.post(f"/posts/{id}/like", headers=auth_headers)
    assert response.status_code == 201

    # removing the like
    response = client.delete(f"/posts/{id}/like", headers=auth_headers)
    assert response.status_code == 204

    # removing it again
    response = client.delete(f"/posts/{id}/like", headers=auth_headers)
    assert response.status_code == 404, "You have to like a post to unlike it"

def test_unlike_post_not_found(client, auth_headers):
    response = client.delete(f"/posts/9999/like", headers=auth_headers)
    assert response.status_code == 404, "Post not found"