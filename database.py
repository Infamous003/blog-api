from sqlmodel import SQLModel, create_engine, Session
import os

# This is the postgres instance url on Render
DATABASE_URL = "postgresql://blogapi_1cft_user:zXEvft6o6b7FqVZvaqgqzgsaoNuFvfXl@dpg-d1ufdf3uibrs738e7i50-a/blogapi_1cft"

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set")

engine = create_engine(DATABASE_URL, echo=True)
def init_db():
    SQLModel.metadata.create_all(engine)

# This function enables us to use Depends and not repeat code by creating
# a session again and agin for each db access
def get_session():
    with Session(engine) as session:
        yield session