from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from sqlalchemy import Column, Text

class Post(SQLModel, table=True):
    __tablename__ = "posts"
    id: int | None = Field(default=None, primary_key=True)
    title: str = Field(nullable=False, max_length=64)
    subtitle: str | None = Field(max_length=128)
    content: str = Field(sa_column=Column(Text))
    created_at: datetime = Field(default_factory=datetime.now)

    username: str = Field(nullable=False)
    user_id: int | None = Field(foreign_key="users.id", ondelete="CASCADE")
    user: list["User"] = Relationship(back_populates="post")

    comment: list["Comment"] = Relationship(back_populates="post")
    like: list["Like"] = Relationship(back_populates="post")


# User models

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: int | None = Field(default=None, primary_key=True)
    username: str = Field(max_length=16, nullable=False, unique=True)
    password: str = Field(max_length=64, min_length=4, nullable=False, unique=False)

    post: Post = Relationship(back_populates="user") # the value of back_populates is the relationship name, not table name
    comment: list["Comment"] = Relationship(back_populates="user")
    like: list["Like"] = Relationship(back_populates="user")


# Comments models

class Comment(SQLModel, table=True):
    __tablename__ = "comments"
    id: int | None = Field(default=None, primary_key=True)
    comment_text: str = Field(max_length=256, nullable=False)

    user_id: int | None = Field(foreign_key="users.id", ondelete="CASCADE")
    post_id: int = Field(foreign_key="posts.id", ondelete="CASCADE")

    post: Post = Relationship(back_populates="comment")
    user: list["User"] = Relationship(back_populates="comment")


# Like model

class Like(SQLModel, table=True):
    __tablename__ = "likes"

    id: int | None = Field(default=None, primary_key=True)

    user_id: int | None = Field(foreign_key="users.id", ondelete="CASCADE")
    post_id: int = Field(foreign_key="posts.id", ondelete="CASCADE")

    user: User = Relationship(back_populates="like")
    post: Post = Relationship(back_populates="like")
