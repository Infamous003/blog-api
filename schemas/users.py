from pydantic import BaseModel

class UserCreate(BaseModel):
    username: str
    password: str

class UserUpdate(UserCreate):
    pass

class UserPublic(BaseModel):
    id: int
    username: str