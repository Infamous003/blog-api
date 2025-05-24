from pydantic import BaseModel
from sqlmodel import SQLModel, Field

class Post(SQLModel, table=True):
    __tablename__ = "posts"
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(nullable=False, max_length=64)
    description: str = Field(nullable=False, max_length=1024)

class PostPublic(BaseModel):
    id: int
    title: str
    description: str

class PostCreate(BaseModel):
    title: str
    description: str

class PostUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

# User models

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(max_length=16, nullable=False, unique=True)
    password: str = Field(max_length=32, min_length=4, nullable=False, unique=False)

class UserCreate(BaseModel):
    username: str
    password: str

class UserUpdate(UserCreate):
    pass

class UserPublic(BaseModel):
    id: int
    username: str
