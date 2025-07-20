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

# This url is the redis instance on render
REDIS_HOST = "redis://red-d1ufcvmr433s73emt4d0"
REDIS_PORT = 6379
# This piece of code will make sure that the db is created before we start making requests
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    app.state.redis = asyncio.Redis(REDIS_HOST, REDIS_PORT)
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
