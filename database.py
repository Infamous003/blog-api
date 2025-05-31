from sqlmodel import SQLModel, create_engine, Session
DATABASE_URL="postgresql://fastapi:BcaZDxm1OmH9QJBq5kSXzxDQruJerr97@dpg-d0sr5l49c44c73ff04mg-a.oregon-postgres.render.com/fastapi_rsus"

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

# This function enables us to use Depends and not repeat code by creating
# a session again and agin for each db access
def get_session():
    with Session(engine) as session:
        yield session