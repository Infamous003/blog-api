from pydantic import BaseModel

class CommentCreate(BaseModel):
    comment_text: str

class CommentUpdate(CommentCreate):
    pass

class CommentPublic(BaseModel):
    id: int
    comment_text: str
    user_id: int
    post_id: int