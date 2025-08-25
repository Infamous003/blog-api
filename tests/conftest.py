from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session
from app import app
from database import get_session
import pytest
from dotenv import load_dotenv
import fakeredis
import asyncio

load_dotenv()

USERNAME = "postgres"
PASSWORD = "password123"
DB_NAME = "test_app"
HOST = "localhost"
PORT = 5432

DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}"

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(DATABASE_URL)
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session):
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    
    app.state.redis = fakeredis.FakeAsyncRedis()
    asyncio.run(app.state.redis.flushall())

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture(name="user_data")
def user_data_fixture():
    return {"username": "test_user", "password": "test_password"}

@pytest.fixture(name="registered_user")
def register_user_fixture(client, user_data):
    response = client.post("/auth/register", json=user_data)
    data = response.json()
    data["password"] = user_data["password"]

    assert response.status_code == 201
    yield data

@pytest.fixture(name="access_token")
def access_token_fixture(client, registered_user):
    response = client.post("/auth/login", data={
        "username": registered_user["username"],
        "password": registered_user["password"]
    })
    assert response.status_code == 200
    data = response.json()
    yield data["access_token"]

@pytest.fixture(name="auth_headers")
def auth_headers_fixture(access_token):
    return {
        "Authorization": f"Bearer {access_token}"
    }

@pytest.fixture(name="post_data")
def post_data_fixture():
    return {"title": "This is some random title, with absolutely no meaning", 
            "subtitle": "Perhaps the subtitle explains it more?",
            "content": "What a shame."}


@pytest.fixture(name="updated_post")
def updated_post_data_fixture():
    return {"title": "Updated title", 
            "subtitle": "Updated subs",
            "content": "NEw content!"}