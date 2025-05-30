from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from sqlmodel import Session, select
from database import engine
from models import User, Post, PostPublic
from datetime import datetime, timedelta, timezone
import jwt


SECRET_KEY = "72a29ca393337573268c0c33b2df524037a40ce0d7b286ef0114d3a83f08e8d2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Helper functions for authentication
def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str):
    with Session(engine) as session:
        query = select(User).where(User.username == username)
        user = session.exec(query).one_or_none()

        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user
    
def authenticate_user(username: str, password: str):
    user = None
    with Session(engine) as session:
        query = select(User).where(User.username == username)
        user = session.exec(query).one_or_none()

    if user is None:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(user_data: dict):
    # user_data dictionary contains the username
    to_encode = user_data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt


# Helper functions for Comments

def get_post_or_404(id: int) -> PostPublic:
    with Session(engine) as session:
        post_found = session.exec(
            select(Post).where(Post.id == id)
        ).one_or_none()

        if post_found is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

        return post_found
