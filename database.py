from sqlmodel import SQLModel, create_engine, Session
# DATABASE_URL = "postgresql://username:password@hostname:port/database_name"

DATABASE_URL = "postgresql://postgres:password@localhost:5432/fastapi"

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

# This function enables us to use Depends and not repeat code by creating
# a session again and agin for each db access
def get_session():
    with Session(engine) as session:
        yield session