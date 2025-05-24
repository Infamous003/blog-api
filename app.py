from fastapi import FastAPI
from database import init_db
from contextlib import asynccontextmanager
import posts

# This piece of code will make sure that the db is created before we start making requests
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(
    title="Blog API",
    description="This is a simple blog api",
    lifespan=lifespan)

app.include_router(posts.router)

@app.get("/")
def root():
    return {"message": "Hello World!"}
