from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship

class Post(SQLModel, table=True):
    __tablename__ = "posts"
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(nullable=False, max_length=64)
    description: str = Field(nullable=False, max_length=1024)

    user_id: int = Field(foreign_key="users.id")
    user: list["User"] = Relationship(back_populates="post")

class PostPublic(BaseModel):
    id: int
    title: str
    description: str
    user_id: int

class PostCreate(BaseModel):
    title: str
    description: str
    user_id: int

class PostUpdate(BaseModel):
    title: str | None = None
    description: str | None = None

# User models

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(max_length=16, nullable=False, unique=True)
    password: str = Field(max_length=64, min_length=4, nullable=False, unique=False)

    post: Post = Relationship(back_populates="user") # the value of back_populates is the relationship name, not table name

class UserCreate(BaseModel):
    username: str
    password: str

class UserUpdate(UserCreate):
    pass

class UserPublic(BaseModel):
    id: int
    username: str


# Authentication models

class Token(BaseModel):
    access_token: str
    token_type: str