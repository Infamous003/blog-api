from fastapi import FastAPI, HTTPException, status, Depends
from models import PostCreate, Post, PostUpdate, PostPublic
from database import init_db, get_sesssion
from sqlmodel import select, Session
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
