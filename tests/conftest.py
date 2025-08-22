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
    # for i in client.app.routes:
    #     print(i)
    # print("---------------------------")
    yield client
    app.dependency_overrides.clear()
