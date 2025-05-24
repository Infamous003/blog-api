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
