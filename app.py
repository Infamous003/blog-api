from fastapi import FastAPI, HTTPException, status
from models import PostCreate, Post, PostUpdate
from database import engine, init_db
from sqlmodel import select, Session

app = FastAPI(title="Blog API", description="This is a simple blog api")

init_db()

@app.get("/")
def root():
    return {"message": "Hello World!"}

@app.get("/posts")
def get_posts():
    with Session(engine) as session:
        query = select(Post)
        posts = session.exec(query).fetchall()

        if not posts:
            return {'message': 'Looks so empty...'}
        return posts

@app.get("/posts/{id}")
def get_posts(id: int):
    with Session(engine) as session:
        query = select(Post).where(Post.id == id)
        post_found = session.exec(query).one_or_none()
        if post_found is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')
        return post_found

@app.post("/posts")
def create_posts(post: PostCreate):
    with Session(engine) as session:
        new_post = Post(**post.model_dump())
        session.add(new_post)
        session.commit()
        session.refresh(new_post)
        return new_post

@app.put("/posts/{id}")
def update_posts(id: int, post: PostUpdate):
    
    with Session(engine) as session:
        query = select(Post).where(Post.id == id)
        post_found = session.exec(query).one_or_none()

        if post_found is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
        
        if post.title: post_found.title = post.title
        if post.description: post_found.description = post.description

        session.add(post_found)
        session.commit()
        session.refresh(post_found)
        return post_found

@app.delete("/posts/{id}")
def delete_posts(id: int):
    with Session(engine) as session:
        query = select(Post).where(Post.id == id)
        post_found = session.exec(query).one_or_none()

        if post_found is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    
        session.delete(post_found)
        session.commit()
        return {'message': 'Post successfully deleted'}