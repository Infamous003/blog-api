from sqlmodel import SQLModel, create_engine
# DATABASE_URL = "postgresql://username:password@hostname:port/database_name"

DATABASE_URL = "postgresql://postgres:password@localhost:5432/fastapi"

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)