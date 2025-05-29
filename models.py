from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship, DateTime
from datetime import datetime

class Post(SQLModel, table=True):
    __tablename__ = "posts"
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(nullable=False, max_length=64)
    subtitle: str | None = Field(max_length=128)
    content: str = Field(nullable=False, max_length=1024)
    created_at: datetime = Field(default_factory=datetime.now)

    user_id: int | None = Field(foreign_key="users.id", ondelete="CASCADE")
    user: list["User"] = Relationship(back_populates="post")

    comment: list["Comment"] = Relationship(back_populates="post")

class PostPublic(BaseModel):
    id: int
    title: str
    subtitle: str
    content: str
    user_id: int

class PostCreate(BaseModel):
    title: str
    subtitle: str | None = None
    content: str


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    subtitle: str | None = None

# User models

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(max_length=16, nullable=False, unique=True)
    password: str = Field(max_length=64, min_length=4, nullable=False, unique=False)

    post: Post = Relationship(back_populates="user") # the value of back_populates is the relationship name, not table name
    comment: list["Comment"] = Relationship(back_populates="user")

class UserCreate(BaseModel):
    username: str
    password: str

class UserUpdate(UserCreate):
    pass

class UserPublic(BaseModel):
    id: int
    username: str

# Comments models

class Comment(SQLModel, table=True):
    __tablename__ = "comments"
    id: int | None = Field(default=None, primary_key=True)
    comment_text: str = Field(max_length=256, nullable=False)

    user_id: int | None = Field(foreign_key="users.id", ondelete="CASCADE")
    post_id: int = Field(foreign_key="posts.id", ondelete="CASCADE")

    post: Post = Relationship(back_populates="comment")
    user: list["User"] = Relationship(back_populates="comment")

class CommentCreate(BaseModel):
    comment_text: str

class CommentUpdate(CommentCreate):
    pass

class CommentPublic(BaseModel):
    id: int
    comment_text: str
    user_id: int


# Authentication models

class Token(BaseModel):
    access_token: str
    token_type: str