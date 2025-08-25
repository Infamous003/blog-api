def test_register_success(client, user_data):
    response = client.post("/auth/register", json=user_data)
    data = response.json()
    assert response.status_code == 201
    assert data["username"] == user_data["username"]

def test_register_conflict(client, registered_user):
    second_response = client.post("/auth/register", json={"username": registered_user["username"], "password": registered_user["password"]})
    assert second_response.status_code == 409, "User already exists"
    
def test_login_success(client, registered_user):
    second_response = client.post("/auth/login", data={"username": registered_user["username"], "password": registered_user["password"]})
    assert second_response.status_code == 200
    assert "access_token" in second_response.json()
    
def test_login_failure(client, user_data):
    second_response = client.post("/auth/login", data=user_data)
    assert second_response.status_code == 401, "Incorrect username or password"
