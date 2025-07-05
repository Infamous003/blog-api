from fastapi import FastAPI
from database import init_db
from contextlib import asynccontextmanager
import routes.posts as posts
# import routes.users as users
import routes.auth as auth
import routes.comments as comments
import routes.likes as likes
from redis import asyncio
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

load_dotenv()

REDIS_HOST = os.getenv("REDIS_HOST")
REDIS_PORT = os.getenv("REDIS_PORT")

# This piece of code will make sure that the db is created before we start making requests
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    app.state.redis = asyncio.Redis(host=REDIS_HOST, port=REDIS_PORT)
    yield
    await app.state.redis.close()

app = FastAPI(
    title="Blog API",
    description="This is a simple blog api",
    lifespan=lifespan)

app.include_router(posts.router)
app.include_router(auth.router)
app.include_router(comments.router)
app.include_router(likes.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "Hello World!"}
