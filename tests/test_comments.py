def test_get_comments(client,
                      created_post,
                      created_comment):
    response = client.get("/comments/")
    data = response.json()

    assert response.status_code == 200
    assert isinstance(data, list)
    assert all(isinstance(post, dict) for post in data)

def test_get_comments_by_post_id_success(client,
                                    created_post,
                                    created_comment):
    id = created_post["id"]
    response = client.get(f"/posts/{id}/comments/")
    data = response.json()[0] # cause it is a list of comments

    assert response.status_code == 200
    assert data["id"] == id
    assert data["comment_text"] == created_comment["comment_text"]

def test_create_comment_success(client,
                                created_post,
                                auth_headers,
                                comment_data):
    id = created_post["id"]
    resp = client.post(f"/posts/{id}/comments", json=comment_data, headers=auth_headers)
    assert resp.status_code == 201

def test_update_comment_success(client,
                                created_post, 
                                created_comment, 
                                auth_headers,
                                updated_comment):
    post_id = created_post["id"]
    comment_id = created_comment["id"]
    resp = client.put(f"/posts/{post_id}/comments/{comment_id}", json=updated_comment, headers=auth_headers)
    data = resp.json()

    assert resp.status_code == 200
    assert data["comment_text"] == updated_comment["comment_text"]


def test_delete_comment_success(client,
                                created_post, 
                                created_comment, 
                                auth_headers):
    post_id = created_post["id"]
    comment_id = created_comment["id"]
    resp = client.delete(f"/posts/{post_id}/comments/{comment_id}", headers=auth_headers)

    assert resp.status_code == 204

# -------- Test cases for 404 errors --------

def test_get_comments_by_post_id_not_found(client):
    response = client.get(f"/posts/9999/comments/")
    assert response.status_code == 404, "Post not found"

def test_create_comment_not_found(client,
                                  auth_headers,
                                  comment_data):
    resp = client.post("/posts/9999/comments", json=comment_data, headers=auth_headers)
    assert resp.status_code == 404, "Comment not found"

def test_update_comment_not_found(client,
                                created_post,  
                                auth_headers,
                                updated_comment):
    post_id = created_post["id"]
    resp = client.put(f"/posts/{post_id}/comments/{9999}", json=updated_comment, headers=auth_headers)
    data = resp.json()

    assert resp.status_code == 404, "Comment not found"

def test_delete_comment_not_found(client,
                                  created_post, 
                                  auth_headers):
    post_id = created_post["id"]
    resp = client.delete(f"/posts/{post_id}/comments/{9999}", headers=auth_headers)

    assert resp.status_code == 404, "Comment not found"

# -------- Test cases for authentication failure --------

def test_create_comment_unauthenticated(client,
                                        created_post,
                                        comment_data):
    id = created_post["id"]
    resp = client.post(f"/posts/{id}/comments", json=comment_data)
    assert resp.status_code == 401, "Not authenticated"

def test_update_comment_unauthenticated(client,
                                        created_post,
                                        created_comment,
                                        updated_comment):
    post_id = created_post["id"]
    comment_id = created_comment["id"]
    resp = client.put(f"/posts/{post_id}/comments/{comment_id}", json=updated_comment)

    assert resp.status_code == 401, "Not authenticated"

def test_delete_comment_unauthenticated(client,
                                        created_post, 
                                        created_comment):
    post_id = created_post["id"]
    comment_id = created_comment["id"]
    resp = client.delete(f"/posts/{post_id}/comments/{comment_id}")

    assert resp.status_code == 401, "Not authenticated"