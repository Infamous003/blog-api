def test_register_success(client):
    user_data = {"username": "test_user", "password": "test_password"}
    
    response = client.post("/auth/register", json=user_data)
    data = response.json()
    assert response.status_code == 201
    assert data["username"] == user_data["username"]

def test_register_conflict(client):
    user_data = {"username": "test_user", "password": "test_password"}
    
    first_response = client.post("/auth/register", json=user_data)
    assert first_response.status_code == 201
    assert first_response.json()["username"] == user_data["username"]

    second_response = client.post("/auth/register", json=user_data)
    assert second_response.status_code == 409, "User already exists"
    
def test_login_success(client):
    user_data = {"username": "test_user", "password": "test_password"}
    
    first_response = client.post("/auth/register", json=user_data)
    assert first_response.status_code == 201
    assert first_response.json()["username"] == user_data["username"]

    second_response = client.post("/auth/login", data=user_data)
    assert second_response.status_code == 200
    
def test_login_failure(client):
    user_data = {"username": "test_user", "password": "test_password"}
    second_response = client.post("/auth/login", data=user_data)

    assert second_response.status_code == 401, "Incorrect username or password"
