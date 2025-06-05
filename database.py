from sqlmodel import SQLModel, create_engine, Session
import os
from dotenv import load_dotenv

# This loads the env variables from .env file
load_dotenv()

USERNAME = os.getenv("DB_USERNAME")
PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")

print(USERNAME, PASSWORD)

# DATABASE_URL = "postgresql://username:password@host:port/database_name"

DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/fastapi"
# print(DATABASE_URL, "------------------------------")
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

# This function enables us to use Depends and not repeat code by creating
# a session again and agin for each db access
def get_session():
    with Session(engine) as session:
        yield session