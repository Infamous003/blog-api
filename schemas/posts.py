from pydantic import BaseModel
from datetime import datetime

class PostPublic(BaseModel):
    id: int
    title: str
    subtitle: str
    content: str
    created_at: datetime
    user_id: int
    username: str

class PostCreate(BaseModel):
    title: str
    subtitle: str | None = None
    content: str


class PostUpdate(BaseModel):
    title: str | None = None
    content: str | None = None
    subtitle: str | None = None